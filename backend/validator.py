def clean(text):
    return text.replace(" ", "").replace("\n", "").lower()

def validar_codigo(user, correct):
    user_clean = clean(user)
    correct_clean = clean(correct)

    # ✅ CORRETO
    if user_clean == correct_clean:
        return True, "🎯 Perfeito! Você acertou exatamente o código!"

    feedback = []

    # 🔍 ANÁLISES INTELIGENTES

    # PRINT / OUTPUT
    if "print" in correct and "print" not in user:
        feedback.append("Você esqueceu de usar print() para exibir o resultado.")

    if "printf" in correct and "printf" not in user:
        feedback.append("Em C você deve usar printf() para mostrar algo na tela.")

    if "echo" in correct and "echo" not in user:
        feedback.append("Em PHP você precisa usar echo para imprimir.")

    if "system.out.println" in correct and "system.out.println" not in user.lower():
        feedback.append("Em Java usamos System.out.println() para imprimir.")

    # MAIN (C / JAVA)
    if "main" in correct and "main" not in user:
        feedback.append("Você esqueceu a função principal main().")

    # INCLUDE (C)
    if "#include" in correct and "#include" not in user:
        feedback.append("Você esqueceu de incluir a biblioteca (#include <stdio.h>).")

    # RETURN (C)
    if "return" in correct and "return" not in user:
        feedback.append("Você esqueceu o return 0 no final do programa.")

    # VARIÁVEL
    if "=" in correct and "=" not in user:
        feedback.append("Você não declarou a variável corretamente.")

    # IF
    if "if" in correct and "if" not in user:
        feedback.append("Você esqueceu a estrutura condicional if.")

    # CHAVES (C/Java)
    if "{" in correct and "{" not in user:
        feedback.append("Você esqueceu de abrir chaves { }.")

    # PARÊNTESES
    if "(" in correct and "(" not in user:
        feedback.append("Você esqueceu os parênteses ().")

    # 💬 RESPOSTA FINAL
    if feedback:
        return False, "🧑‍🏫 Professor diz:\n\n- " + "\n- ".join(feedback)

    return False, "❌ Quase! Revise a sintaxe e tente novamente."
