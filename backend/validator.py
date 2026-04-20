def limpar(texto):
    return texto.replace(" ", "").replace("\n", "").lower()

def validar_codigo(resposta_usuario, resposta_correta):
    if limpar(resposta_usuario) == limpar(resposta_correta):
        return True, "Perfeito! Você acertou 🎯"

    # feedback inteligente
    if "printf" in resposta_correta and "printf" not in resposta_usuario:
        return False, "Você esqueceu o printf!"

    if "print" in resposta_correta and "print" not in resposta_usuario:
        return False, "Você esqueceu o print!"

    if "system.out.println" in resposta_correta and "system.out.println" not in resposta_usuario.lower():
        return False, "Você esqueceu o System.out.println!"

    if "echo" in resposta_correta and "echo" not in resposta_usuario:
        return False, "Você esqueceu o echo!"

    return False, "Quase! Revise o código."
