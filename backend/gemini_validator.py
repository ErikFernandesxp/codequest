import os
import urllib.request
import json
import re

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


def _get_key() -> str:
    return os.getenv("GEMINI_KEY", "")


def _validacao_rapida(resposta: str, linguagem: str) -> tuple[bool, str]:
    linhas = resposta.strip().split("\n")

    if linguagem == "python":
        for linha in linhas:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue

            match = re.match(r'^(\w+)\s*=\s*([^"\'\d\[\{(].+)$', linha)
            if match:
                valor = match.group(2).strip()
                if not re.match(
                    r'^(True|False|None|int|float|str|list|dict|\[|\{|\()',
                    valor
                ):
                    return True, (
                        "Strings precisam estar entre aspas. "
                        "Ex: nome = 'João' e não nome = João"
                    )

            match_print = re.match(r"^print\(['\"](\w+)['\"]\)$", linha)
            if match_print:
                var_dentro = match_print.group(1)
                if re.search(r'\b' + var_dentro + r'\s*=', resposta):
                    return True, (
                        f"print('{var_dentro}') imprime a palavra '{var_dentro}', "
                        f"não o valor da variável. "
                        f"Use print({var_dentro}) sem aspas."
                    )

    return False, ""


def _fallback_restrito(resposta_aluno, gabarito, respostas_aceitas, keywords):
    from backend.validator import validar_codigo

    correto, feedback = validar_codigo(
        resposta_aluno, gabarito,
        respostas_aceitas=respostas_aceitas,
        keywords=None  # sem keywords no fallback — mais seguro
    )
    if correto:
        return True, feedback

    if keywords:
        tem_estrutura = (
            ("(" in resposta_aluno and ")" in resposta_aluno)
            or "=" in resposta_aluno
        )
        if tem_estrutura:
            correto, feedback = validar_codigo(
                resposta_aluno, gabarito,
                respostas_aceitas=respostas_aceitas,
                keywords=keywords
            )
            if correto:
                return True, feedback

    return False, "Verifique a sintaxe e tente novamente."


def validar_com_gemini(pergunta, resposta_aluno, linguagem):
    key = _get_key()
    if not key:
        return None, "sem_key"

    prompt = (
        "Você é um professor rigoroso de programação avaliando um aluno iniciante.\n\n"
        f"Linguagem: {linguagem.upper()}\n"
        f"Pergunta: {pergunta}\n"
        f"Resposta do aluno:\n{resposta_aluno}\n\n"
        "CONSIDERE CORRETO apenas se:\n"
        "- Código executaria sem erros\n"
        "- Lógica resolve exatamente o pedido\n"
        "- Sintaxe 100% correta\n"
        "- Strings entre aspas\n"
        "- Variáveis usadas corretamente\n\n"
        "CONSIDERE INCORRETO se:\n"
        "- Strings sem aspas: nome = João → ERRADO\n"
        "- print('nome') quando deveria ser print(nome) → ERRADO\n"
        "- Qualquer erro de sintaxe\n"
        "- Não resolve o que foi pedido\n"
        "- Só o resultado sem código: ex: escrever 'Ola' em vez de print('Ola')\n"
        "- Código incompleto\n\n"
        "Simule a execução. Se causaria erro, é INCORRETO.\n\n"
        'Responda APENAS em JSON sem markdown:\n'
        '{"correto": true, "feedback": "Frase curta do que está certo."}\n'
        'ou\n'
        '{"correto": false, "feedback": "Frase curta do erro e como corrigir."}'
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
    pergunta, resposta_aluno, linguagem, gabarito,
    respostas_aceitas=None, keywords=None
):
    # 1. Erros óbvios de sintaxe
    tem_erro, msg_erro = _validacao_rapida(resposta_aluno, linguagem)
    if tem_erro:
        return False, msg_erro, "local"

    # 2. Gemini
    if _get_key():
        correto, feedback = validar_com_gemini(pergunta, resposta_aluno, linguagem)
        if correto is not None:
            return correto, feedback, "gemini"

    # 3. Fallback restrito só quando Gemini falhou
    correto, feedback = _fallback_restrito(
        resposta_aluno, gabarito,
        respostas_aceitas or [], keywords or []
    )
    return correto, feedback, "local"
