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


def _normalizar(texto: str) -> str:
    """Remove espaços extras mas preserva estrutura."""
    linhas = [l.strip() for l in texto.strip().splitlines() if l.strip()]
    return "\n".join(linhas)


def _validacao_local_rigorosa(resposta: str, linguagem: str, gabarito: str) -> tuple:
    """
    Validação local RIGOROSA.
    Retorna (True/False/None, mensagem)
    None = passa pro Gemini decidir
    """
    resp = resposta.strip()
    gab  = gabarito.strip()

    if not resp:
        return False, "Resposta vazia."

    linhas_gab  = [l.strip() for l in gab.splitlines()  if l.strip()]
    linhas_resp = [l.strip() for l in resp.splitlines() if l.strip()]

    # ── Quantidade de linhas ─────────────────────────────────────────────────
    if len(linhas_resp) < len(linhas_gab):
        faltam = len(linhas_gab) - len(linhas_resp)
        return False, (
            f"Resposta incompleta! Faltam {faltam} linha(s). "
            f"A solução completa precisa de {len(linhas_gab)} linha(s)."
        )

    resp_lower = resp.lower()

    # ── PYTHON ───────────────────────────────────────────────────────────────
    if linguagem == "python":
        # P maiúsculo no Print
        if re.search(r'\bPrint\b|\bPRINT\b', resp):
            return False, "Em Python use print() com todas as letras minúsculas."

        # String sem aspas: nome = João
        for linha in linhas_resp:
            match = re.match(r'^(\w+)\s*=\s*([^"\'\d\[\{(].+)$', linha)
            if match:
                valor = match.group(2).strip()
                if not re.match(
                    r'^(True|False|None|int|float|str|list|dict|input|\[|\{|\()',
                    valor
                ):
                    return False, (
                        "Strings precisam estar entre aspas. "
                        "Ex: nome = 'João' e não nome = João"
                    )

        # print('variavel') em vez de print(variavel)
        for linha in linhas_resp:
            m = re.match(r"^print\(['\"](\w+)['\"]\)$", linha)
            if m:
                var = m.group(1)
                if re.search(r'\b' + var + r'\s*=', resp):
                    return False, (
                        f"print('{var}') imprime a palavra '{var}'. "
                        f"Use print({var}) sem aspas para exibir o valor da variável."
                    )

    # ── JAVA ─────────────────────────────────────────────────────────────────
    elif linguagem == "java":
        # S maiúsculo em System
        if "system.out" in resp_lower and "System.out" not in resp:
            return False, "Em Java use System com S maiúsculo: System.out.println()"

        # println minúsculo
        if re.search(r'System\.out\.(?!println|print\b)[Pp]rint', resp):
            return False, "Use System.out.println() com letras minúsculas."

        # Ponto e vírgula obrigatório ao final de cada instrução
        for linha in linhas_resp:
            if linha and not linha.endswith((";", "{", "}", "//")):
                # Ignora linhas que são só comentários ou estruturas
                if re.search(r'System\.out\.|int |String |double |boolean ', linha):
                    return False, (
                        f"Falta ponto e vírgula no final: '{linha}'\n"
                        "Em Java toda instrução termina com ;"
                    )

        # Verifica se o texto exibido bate com o gabarito
        textos_gab  = re.findall(r'println\("([^"]+)"\)|print\("([^"]+)"\)', gab)
        textos_resp = re.findall(r'println\("([^"]+)"\)|print\("([^"]+)"\)', resp)
        textos_gab  = [a or b for a, b in textos_gab]
        textos_resp = [a or b for a, b in textos_resp]

        if textos_gab and textos_resp:
            for t in textos_gab:
                if t not in textos_resp:
                    return False, (
                        f"O texto exibido está errado. "
                        f"Esperado: \"{t}\""
                    )

    # ── C ────────────────────────────────────────────────────────────────────
    elif linguagem == "c":
        # printf minúsculo
        if re.search(r'\bPrintf\b|\bPRINTF\b', resp):
            return False, "Em C use printf() com letras minúsculas."

        # Ponto e vírgula obrigatório
        for linha in linhas_resp:
            if linha and not linha.endswith((";", "{", "}", "*/")):
                if re.search(r'printf|scanf|int |float |char |return', linha):
                    return False, (
                        f"Falta ponto e vírgula: '{linha}'\n"
                        "Em C toda instrução termina com ;"
                    )

        # #include obrigatório se gabarito tem
        if "#include" in gab and "#include" not in resp:
            return False, "Falta o #include no início do programa C."

        # Verifica texto exibido
        textos_gab  = re.findall(r'printf\("([^"\\]+)', gab)
        textos_resp = re.findall(r'printf\("([^"\\]+)', resp)
        if textos_gab and textos_resp:
            for t in textos_gab:
                t_limpo = t.replace("\\n", "").strip()
                if t_limpo and not any(t_limpo in r for r in textos_resp):
                    return False, (
                        f"O texto exibido está errado. "
                        f"Esperado: \"{t_limpo}\""
                    )

    # ── PHP ──────────────────────────────────────────────────────────────────
    elif linguagem == "php":
        # <?php obrigatório se gabarito tem
        if "<?php" in gab and "<?php" not in resp:
            return False, "Falta a tag <?php no início do código PHP."

        # echo minúsculo
        if re.search(r'\bEcho\b|\bECHO\b', resp):
            return False, "Em PHP use echo com letras minúsculas."

        # Ponto e vírgula obrigatório
        for linha in linhas_resp:
            if linha and not linha.endswith((";", "{", "}", "?>", "/*", "*/")):
                if re.search(r'\becho\b|\$\w+\s*=', linha):
                    return False, (
                        f"Falta ponto e vírgula: '{linha}'\n"
                        "Em PHP toda instrução termina com ;"
                    )

        # Verifica texto exibido
        textos_gab  = re.findall(r'echo\s+["\']([^"\']+)["\']', gab)
        textos_resp = re.findall(r'echo\s+["\']([^"\']+)["\']', resp)
        if textos_gab and textos_resp:
            for t in textos_gab:
                if t not in textos_resp:
                    return False, (
                        f"O texto exibido está errado. "
                        f"Esperado: \"{t}\""
                    )

    return None, ""  # Passa pro Gemini


def _fallback_restrito(resposta_aluno, gabarito, respostas_aceitas):
    from backend.validator import validar_codigo
    correto, feedback = validar_codigo(
        resposta_aluno, gabarito,
        respostas_aceitas=respostas_aceitas,
        keywords=None
    )
    return correto, feedback


def validar_com_gemini(pergunta, resposta_aluno, linguagem, gabarito, respostas_aceitas):
    key = _get_key()
    if not key:
        return None, "sem_key"

    exemplos = gabarito
    if respostas_aceitas:
        exemplos += "\n" + "\n".join(respostas_aceitas[:3])

    prompt = (
        f"Você é um professor RIGOROSO de {linguagem.upper()} avaliando um aluno iniciante.\n\n"
        f"Pergunta: {pergunta}\n\n"
        f"RESPOSTA CORRETA ESPERADA:\n{exemplos}\n\n"
        f"RESPOSTA DO ALUNO:\n{resposta_aluno}\n\n"
        "SEJA EXTREMAMENTE RIGOROSO. Considere INCORRETO se:\n"
        "- O texto/valor exibido for diferente do esperado (qualquer diferença)\n"
        "- Falta ponto e vírgula onde é obrigatório (Java, C, PHP)\n"
        "- Letras maiúsculas/minúsculas erradas onde importa\n"
        "- Falta qualquer linha da solução completa\n"
        "- Usa função errada (ex: print em vez de println em Java)\n"
        "- Tem erro de sintaxe que causaria falha na execução\n"
        "- Escreveu só o resultado sem o código (ex: 'Olá' em vez de print('Olá'))\n"
        "- Código incompleto\n\n"
        "Considere CORRETO APENAS se:\n"
        "- O código executaria sem erros\n"
        "- Produz exatamente o resultado pedido\n"
        "- Aspas simples ou duplas são equivalentes\n"
        "- Espaços extras irrelevantes são aceitáveis\n\n"
        "Responda APENAS em JSON sem markdown:\n"
        '{"correto": true, "feedback": "Frase curta do que está certo."}\n'
        'ou\n'
        '{"correto": false, "feedback": "Erro específico e como corrigir."}'
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
    # 1. Validação local rigorosa — pega erros óbvios de todas as linguagens
    correto, msg = _validacao_local_rigorosa(resposta_aluno, linguagem, gabarito)
    if correto is not None:
        return correto, msg, "local"

    # 2. Gemini com gabarito e prompt rigoroso
    if _get_key():
        correto, feedback = validar_com_gemini(
            pergunta, resposta_aluno, linguagem,
            gabarito, respostas_aceitas or []
        )
        if correto is not None:
            return correto, feedback, "gemini"

    # 3. Fallback só quando Gemini falhou — sem keywords
    correto, feedback = _fallback_restrito(
        resposta_aluno, gabarito, respostas_aceitas or []
    )
    return correto, feedback, "local"
