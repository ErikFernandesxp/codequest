import os
import urllib.request
import urllib.error
import json


GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


def _get_key() -> str:
    return os.getenv("GEMINI_KEY", "")


def _tem_internet() -> bool:
    """Verifica rapidamente se há conexão com a internet."""
    try:
        urllib.request.urlopen("https://www.google.com", timeout=2)
        return True
    except Exception:
        return False


def validar_com_gemini(pergunta: str, resposta_aluno: str, linguagem: str) -> tuple[bool, str]:
    """
    Valida a resposta do aluno usando o Gemini.
    Retorna (correto: bool, feedback: str)
    """
    key = _get_key()
    if not key:
        return None, "sem_key"

    prompt = f"""Você é um professor de programação avaliando a resposta de um aluno iniciante.

Linguagem: {linguagem.upper()}
Pergunta do exercício: {pergunta}
Resposta do aluno: {resposta_aluno}

Avalie se a resposta do aluno resolve corretamente o que foi pedido.
Considere correto se:
- A lógica está certa, mesmo que use nomes de variáveis diferentes
- Usa aspas simples ou duplas (ambas válidas)
- Tem espaços extras ou estilo diferente mas funciona
- Usa uma abordagem alternativa válida que resolva o problema

Responda APENAS neste formato JSON (sem markdown, sem explicação):
{{"correto": true, "feedback": "Muito bem! Explicação curta do que o aluno fez certo."}}
ou
{{"correto": false, "feedback": "Explicação curta e encorajadora do que está errado e como corrigir."}}"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 200}
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{GEMINI_API_URL}?key={key}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
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
    """
    Validação combinada: tenta Gemini primeiro, cai no validador local se falhar.
    Retorna (correto: bool, feedback: str, fonte: str)
    fonte pode ser: 'gemini', 'local'
    """
    from backend.validator import validar_codigo

    # Tenta Gemini se tiver internet e key
    if _get_key() and _tem_internet():
        correto, feedback = validar_com_gemini(pergunta, resposta_aluno, linguagem)
        if correto is not None:
            return correto, feedback, "gemini"

    # Fallback: validador local
    correto, feedback = validar_codigo(
        resposta_aluno, gabarito,
        respostas_aceitas=respostas_aceitas,
        keywords=keywords
    )
    return correto, feedback, "local"
