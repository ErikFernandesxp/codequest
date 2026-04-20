def validar_codigo(resposta_usuario, resposta_correta):
    r_user = resposta_usuario.replace(" ", "").replace("\n", "")
    r_ok = resposta_correta.replace(" ", "").replace("\n", "")

    if r_user == r_ok:
        return True, "Perfeito! Código completo correto 🎯"

    if "main" in resposta_correta and "main" not in resposta_usuario:
        return False, "Você esqueceu a função main!"

    if "#include" in resposta_correta and "#include" not in resposta_usuario:
        return False, "Faltou incluir a biblioteca!"

    if "return" in resposta_correta and "return" not in resposta_usuario:
        return False, "Você esqueceu o return!"

    return False, "Quase! Revise a estrutura completa do código."
