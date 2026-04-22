def init_session(st):
    defaults = {
        "logado": False,
        "usuario": "",
        "xp": 0,
        "nivel": 1,
        "fase": 0,
        "linguagem": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value