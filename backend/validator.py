def clean(text):
    return text.replace(" ", "").replace("\n", "").lower()

def validar_codigo(user, correct):
    user_clean = clean(user)
    correct_clean = clean(correct)

    if user_clean == correct_clean:
        return True, "🎯 Perfeito! Código correto!"

    feedback = []

    if "print" in correct and "print" not in user:
        feedback.append("Use print()")

    if "printf" in correct and "printf" not in user:
        feedback.append("Use printf()")

    if "echo" in correct and "echo" not in user:
        feedback.append("Use echo")

    if "main" in correct and "main" not in user:
        feedback.append("Faltou main()")

    if "#include" in correct and "#include" not in user:
        feedback.append("Faltou #include <stdio.h>")

    if "return" in correct and "return" not in user:
        feedback.append("Faltou return 0")

    if feedback:
        return False, "🧑‍🏫 Professor:\n\n- " + "\n- ".join(feedback)

    return False, "❌ Revise o código"
