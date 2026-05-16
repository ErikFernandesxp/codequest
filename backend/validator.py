import re


def clean(text: str) -> str:
    return (
        text.strip()
        .replace(" ", "")
        .replace("\n", "")
        .replace('"', "'")  # normaliza aspas mas não remove
        .lower()
    )


def clean_total(text: str) -> str:
    """Remove tudo incluindo aspas — para comparação estrutural."""
    return (
        text.strip()
        .replace(" ", "")
        .replace("\n", "")
        .replace('"', "")
        .replace("'", "")
        .lower()
    )


def validar_codigo(user: str, correct: str, respostas_aceitas=None, keywords=None):
    user_clean = clean(user)

    # 1. Comparação direta (normaliza aspas mas mantém estrutura)
    if clean(correct) and user_clean == clean(correct):
        return True, "Perfeito!"

    # 2. Comparação sem aspas (aceita simples ou duplas)
    if clean_total(correct) and clean_total(user) == clean_total(correct):
        return True, "Perfeito!"

    # 3. Respostas alternativas aceitas
    if respostas_aceitas:
        for alternativa in respostas_aceitas:
            if clean_total(user) == clean_total(alternativa):
                return True, "Perfeito!"

    # 4. Keywords — MUITO mais rígido agora
    # Só aprova se keywords estão presentes E o código tem estrutura mínima válida
    if keywords:
        user_lower = user.lower().strip()
        keywords_faltando = [kw for kw in keywords if kw.lower() not in user_lower]

        if not keywords_faltando:
            # Verifica estrutura mínima — não pode ser só palavras soltas
            tem_estrutura = (
                "(" in user and ")" in user  # tem chamada de função
                or "=" in user               # tem atribuição
                or "{" in user               # tem bloco
            )
            # Verifica tamanho mínimo — evita cola de palavra avulsa
            tamanho_minimo = len(user.strip()) >= 5

            if tem_estrutura and tamanho_minimo:
                return True, "Perfeito!"

    # 5. Feedback específico
    feedback = []
    if "print" in correct and "print" not in user:
        feedback.append("Você esqueceu de usar print()")
    if "printf" in correct and "printf" not in user:
        feedback.append("Você precisa usar printf()")
    if "echo" in correct and "echo" not in user:
        feedback.append("Use echo para exibir texto em PHP")
    if "for" in correct and "for" not in user:
        feedback.append("Use um loop for")
    if "if" in correct and "if" not in user:
        feedback.append("Use uma estrutura if")
    if "def" in correct and "def" not in user:
        feedback.append("Crie uma função com def")
    if "return" in correct and "return" not in user:
        feedback.append("Não esqueça do return")

    if feedback:
        return False, " | ".join(feedback)
    return False, "Revise a sintaxe"
