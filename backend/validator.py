def clean(text):
    return text.replace(" ", "").replace("\n", "").lower()

def validar_codigo(user, correct):
    if clean(user) == clean(correct):
        return True, "🎯 Perfeito!"

    dicas = []

    if "print" in correct and "print" not in user:
        dicas.append("Use print()")

    if "printf" in correct and "printf" not in user:
        dicas.append("Use printf()")

    if "echo" in correct and "echo" not in user:
        dicas.append("Use echo")

    if "main" in correct and "main" not in user:
        dicas.append("Faltou main()")

    if dicas:
        return False, "💡 Dicas: " + ", ".join(dicas)

    return False, "❌ Revise o código"
