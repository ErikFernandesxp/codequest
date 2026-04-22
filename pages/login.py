import streamlit as st

st.set_page_config(page_title="CodeQuest", layout="wide")

if "logado" not in st.session_state:
    st.session_state["logado"] = False

st.title("🔐 CodeQuest - Login")

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
            "linguagem": None
        })
        st.success("Login realizado 🚀")
        st.switch_page("dashboard")
    else:
        st.error("Preencha todos os campos")
