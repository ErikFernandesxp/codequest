def clean(text):
    return (
        text.replace(" ", "")
        .replace("\n", "")
        .replace('"', "")
        .replace("'", "")
        .lower()
    )

def validar_codigo(user, correct):
    if clean(user) == clean(correct):
        return True, "Perfeito!"

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
