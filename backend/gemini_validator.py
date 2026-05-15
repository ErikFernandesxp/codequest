import os
import urllib.request
import json
import re

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent
)

def _get_key() -> str:
    return os.getenv("GEMINI_KEY", "")


def _validacao_rapida(resposta: str, linguagem: str) -> tuple[bool, str]:
    """
    Validação rápida de erros óbvios ANTES de chamar o Gemini.
    Retorna (tem_erro: bool, mensagem: str)
    """
    linhas = resposta.strip().split("\n")

    if linguagem == "python":
        for linha in linhas:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue

            # Verifica atribuição de string sem aspas
            # ex: nome = João (sem aspas em volta de João)
            match = re.match(r'^(\w+)\s*=\s*([^"\'\d\[\{(True|False|None].+)$', linha)
            if match:
                valor = match.group(2).strip()
                # Se não começa com aspas, número, colchete, parêntese ou palavra reservada
                if not re.match(r'^[\"\'\d\[\{\(]|^(True|False|None|int|float|str|list|dict)', valor):
                    return True, "Atenção! Strings precisam estar entre aspas. Ex: nome = 'João' e não nome = João"

            # Verifica print('variavel') quando deveria ser print(variavel)
            # Detecta print com string que bate com nome de variável declarada
            match_print = re.match(r"^print\(['\"](\w+)['\"]\)$", linha)
            if match_print:
                var_dentro = match_print.group(1)
                # Verifica se essa palavra é uma variável declarada no código
                if re.search(r'\b' + var_dentro + r'\s*=', resposta):
                    return True, (
                        "Atenção! print('" + var_dentro + "') imprime a palavra '" + var_dentro + "' e não o valor da variável. "
                        "Use print(" + var_dentro + ") sem aspas para exibir o valor da variável."
                    )

    return False, ""


def validar_com_gemini(pergunta: str, resposta_aluno: str, linguagem: str) -> tuple[bool, str]:
    key = _get_key()
    if not key:
        return None, "sem_key"

    prompt = (
        "Você é um professor rigoroso de programação avaliando a resposta de um aluno iniciante.\n\n"
        "Linguagem: " + linguagem.upper() + "\n"
        "Pergunta do exercício: " + pergunta + "\n"
        "Resposta do aluno:\n" + resposta_aluno + "\n\n"
        "REGRAS DE AVALIAÇÃO:\n\n"
        "CONSIDERE CORRETO apenas se:\n"
        "- O código funcionaria sem erros se executado agora\n"
        "- A lógica resolve exatamente o que foi pedido\n"
        "- A sintaxe da linguagem está 100% correta\n"
        "- Strings estão entre aspas (simples ou duplas)\n"
        "- Variáveis são usadas corretamente (sem aspas ao imprimir)\n\n"
        "CONSIDERE INCORRETO se:\n"
        "- Strings sem aspas: nome = João em vez de nome = 'Joao'\n"
        "- Variável impressa como string: print('nome') quando deveria ser print(nome)\n"
        "- Qualquer erro de sintaxe que causaria falha na execução\n"
        "- O código não resolve exatamente o que foi pedido\n"
        "- Typos que mudam o comportamento: 'BBem-vindo' tem dois B, está errado\n"
        "- O aluno escreveu só o resultado esperado sem código (ex: 'Ola' em vez de print('Ola'))\n\n"
        "Simule mentalmente a execução do código. Se causaria erro ou resultado errado, é INCORRETO.\n\n"
        'Responda APENAS neste formato JSON sem markdown:\n'
        '{"correto": true, "feedback": "Frase curta sobre o que o aluno fez certo."}\n'
        'ou\n'
        '{"correto": false, "feedback": "Frase curta sobre o erro especifico e como corrigir."}'
    )

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 200}
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{GEMINI_API_URL}?key={key}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            texto = data["candidates"][0]["content"]["parts"][0]["text"]
            texto = texto.strip().replace("```json", "").replace("```", "").strip()
            resultado = json.loads(texto)
            return resultado.get("correto", False), resultado.get("feedback", "")
    except Exception:
        return None, "erro_api"


def validar_resposta(
    pergunta: str,
    resposta_aluno: str,
    linguagem: str,
    gabarito: str,
    respostas_aceitas: list = None,
    keywords: list = None
) -> tuple[bool, str, str]:
    from backend.validator import validar_codigo

    # 1. Validação rápida local — pega erros óbvios antes do Gemini
    tem_erro, msg_erro = _validacao_rapida(resposta_aluno, linguagem)
    if tem_erro:
        return False, msg_erro, "local"

    # 2. Tenta Gemini
    if _get_key():
        correto, feedback = validar_com_gemini(pergunta, resposta_aluno, linguagem)
        if correto is not None:
            return correto, feedback, "gemini"

    # 3. Fallback: validador local
    correto, feedback = validar_codigo(
        resposta_aluno, gabarito,
        respostas_aceitas=respostas_aceitas,
        keywords=keywords
    )
    return correto, feedback, "local"
