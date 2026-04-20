def validar_codigo(resposta_usuario, resposta_correta):
    resposta_usuario = resposta_usuario.strip()

    if resposta_usuario == resposta_correta.strip():
        return True, "Perfeito! Você acertou 🎯"

    # feedback inteligente
    if "printf" in resposta_correta and "printf" not in resposta_usuario:
        return False, "Você esqueceu de usar printf!"

    if ";" in resposta_correta and ";" not in resposta_usuario:
        return False, "Não esqueça do ponto e vírgula!"

    if "print" in resposta_correta and "print" not in resposta_usuario:
        return False, "Você esqueceu o print!"

    return False, "Quase! Revise a sintaxe e tente novamente."
