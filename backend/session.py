def init_session(st):
    defaults = {
        "logado": True,
        "usuario": "guest",
        "xp": 0,
        "nivel": 1,
        "fase": 0,
        "linguagem": None,
        "desafio_atual": 0,
        "vidas": 3
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
