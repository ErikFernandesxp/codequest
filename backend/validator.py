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
        feedback.append("Use print()")

    if "printf" in correct and "printf" not in user:
        feedback.append("Use printf()")

    if "echo" in correct and "echo" not in user:
        feedback.append("Use echo")

    if "for" in correct and "for" not in user:
        feedback.append("Use for")

    if "if" in correct and "if" not in user:
        feedback.append("Use if")

    if feedback:
        return False, "Professor:\n- " + "\n- ".join(feedback)

    return False, "Revise a sintaxe"
