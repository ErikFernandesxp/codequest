def validar_codigo(resposta_usuario, resposta_correta):
    if resposta_usuario.strip() == resposta_correta.strip():
        return True, "Perfeito! Você acertou 🎯"
    else:
        return False, f"Erro! O correto seria:\n{resposta_correta}"