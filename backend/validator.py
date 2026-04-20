def validar_codigo(resposta_usuario, resposta_correta):
    if resposta_usuario.strip() == resposta_correta.strip():
        return True, "Perfeito! Você entendeu 🎯"

    if "printf" not in resposta_usuario:
        return False, "Você esqueceu de usar printf!"

    if ";" not in resposta_usuario:
        return False, "Em C, não esqueça do ponto e vírgula!"

    return False, "Quase! Revise a sintaxe e tente novamente."
