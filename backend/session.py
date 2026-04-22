def init_session(st):
    defaults = {
        "logado": False,
        "usuario": "",
        "xp": 0,
        "nivel": 1,
        "fase": 0,
        "linguagem": None,
        "desafio_atual": 0,
        "acertos_fase": 0
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
