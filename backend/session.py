def init_session(st):

    defaults = {
        "logado": False,
        "usuario": None,
        "usuarios": {},
        "linguagem": None,
        "fase": 0,
        "desafio_atual": 0,
        "xp": 0,
        "nivel": 1,
        "vidas": 3
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
