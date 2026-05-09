import os
import urllib.request
import json

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)

def _get_key() -> str:
    return os.getenv("GEMINI_KEY", "")


def validar_com_gemini(pergunta: str, resposta_aluno: str, linguagem: str) -> tuple[bool, str]:
    key = _get_key()
    if not key:
        return None, "sem_key"

    prompt = f"""Você é um professor rigoroso de programação avaliando a resposta de um aluno iniciante.

Linguagem: {linguagem.upper()}
Pergunta do exercício: {pergunta}
Resposta do aluno:
{resposta_aluno}

REGRAS DE AVALIAÇÃO — leia com atenção:

CONSIDERE CORRETO apenas se:
- O código funcionaria sem erros se executado
- A lógica resolve exatamente o que foi pedido
- A sintaxe da linguagem está correta
- Variáveis são declaradas corretamente antes de serem usadas
- Strings estão entre aspas (simples ou duplas, ambas válidas)
- Funções são chamadas corretamente (ex: print(variavel) e não print('variavel'))

CONSIDERE INCORRETO se:
- Strings não estão entre aspas (ex: nome = João em vez de nome = 'João')
- Variável sendo impressa como string literal (ex: print('nome') quando deveria ser print(nome))
- Sintaxe errada que causaria erro de execução
- O código não resolve o que foi pedido
- Falta parênteses, aspas, dois pontos ou outro elemento obrigatório
- O aluno digitou só o resultado esperado em vez do código (ex: escreveu "Olá" em vez de print("Olá"))
- Typos que mudariam o comportamento (ex: 'BBem-vindo' tem dois B, está errado)

ATENÇÃO ESPECIAL:
- print('nome') imprime a string 'nome', NAO o valor da variável nome
- print(nome) imprime o valor da variável nome — são coisas DIFERENTES
- nome = João sem aspas é erro de sintaxe em Python
- Avalie o código como um interpretador faria — sem tolerância a erros de sintaxe

Responda APENAS neste formato JSON sem markdown:
{{"correto": true, "feedback": "Muito bem! Explique em uma frase o que o aluno fez certo."}}
ou
{{"correto": false, "feedback": "Explique em uma frase o erro especifico e como corrigir, de forma encorajadora."}}"""

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

    if _get_key():
        correto, feedback = validar_com_gemini(pergunta, resposta_aluno, linguagem)
        if correto is not None:
            return correto, feedback, "gemini"

    correto, feedback = validar_codigo(
        resposta_aluno, gabarito,
        respostas_aceitas=respostas_aceitas,
        keywords=keywords
    )
    return correto, feedback, "local"
