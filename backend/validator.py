def clean(text):
    return (
        text.replace(" ", "")
        .replace("\n", "")
        .replace('"', "")
        .replace("'", "")
        .lower()
    )


def validar_codigo(user, correct, respostas_aceitas=None, keywords=None):
    user_clean = clean(user)

    # 1. Verifica contra a resposta principal
    if clean(correct) and user_clean == clean(correct):
        return True, "Perfeito!"

    # 2. Verifica contra respostas alternativas aceitas
    if respostas_aceitas:
        for alternativa in respostas_aceitas:
            if user_clean == clean(alternativa):
                return True, "Perfeito!"

    # 3. Verifica keywords obrigatórias (se definidas, todas precisam estar presentes)
    if keywords:
        user_lower = user.lower()
        keywords_faltando = [kw for kw in keywords if kw.lower() not in user_lower]
        if not keywords_faltando:
            return True, "Perfeito!"

    # 4. Feedback específico por padrão de erro
    feedback = []

    if "print" in correct and "print" not in user:
        feedback.append("Você esqueceu de usar print()")

    if "printf" in correct and "printf" not in user:
        feedback.append("Você precisa usar printf()")

    if "echo" in correct and "echo" not in user:
        feedback.append("Use echo para exibir texto")

    if "for" in correct and "for" not in user:
        feedback.append("Use um loop for")

    if "if" in correct and "if" not in user:
        feedback.append("Use uma estrutura if")

    if feedback:
        return False, "\n".join(feedback)

    return False, "Revise a sintaxe geral"
