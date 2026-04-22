import streamlit as st
from backend.session import init_session

init_session(st)

st.title("📝 Criar Conta")

usuarios = st.session_state.get("usuarios", {})

nome = st.text_input("👤 Nome")
email = st.text_input("📧 Email")
senha = st.text_input("🔒 Senha", type="password")

if st.button("Cadastrar"):

    if not nome or not email or not senha:
        st.error("Preencha todos os campos")
        st.stop()

    if email in usuarios:
        st.error("Email já cadastrado")
        st.stop()

    # salva usuário
    usuarios[email] = {
        "nome": nome,
        "senha": senha,
        "xp": 0,
        "nivel": 1
    }

    st.session_state["usuarios"] = usuarios

    st.success("Conta criada com sucesso! 🎉")

    st.switch_page("pages/login.py")