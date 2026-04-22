import streamlit as st
from backend.session import init_session

init_session(st)

st.title("🔐 Login")

usuarios = st.session_state.get("usuarios", {})

email = st.text_input("📧 Email")
senha = st.text_input("🔒 Senha", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("Entrar"):

        if email in usuarios and usuarios[email]["senha"] == senha:
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuarios[email]["nome"]

            st.success("Login realizado!")
            st.switch_page("pages/linguagem.py")
        else:
            st.error("Email ou senha incorretos")

with col2:
    if st.button("Criar Conta"):
        st.switch_page("pages/cadastro.py")
