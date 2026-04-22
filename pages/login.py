import streamlit as st
from backend.session import init_session

init_session(st)

st.set_page_config(page_title="CodeQuest", layout="wide")

st.title("🔐 CodeQuest Login")

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    if usuario and senha:
        st.session_state.update({
            "logado": True,
            "usuario": usuario,
            "xp": 0,
            "nivel": 1,
            "fase": 0,
            "linguagem": None,
            "desafio_atual": 0,
            "acertos_fase": 0
        })
        st.switch_page("pages/dashboard.py")
    else:
        st.error("Preencha os campos")
