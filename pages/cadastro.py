import streamlit as st

st.set_page_config(page_title="CodeQuest - Cadastro", page_icon="📝", layout="centered")

from backend.session import init_session
from backend.crud import registrar_usuario

init_session(st)

if st.session_state.get("logado"):
    st.switch_page("pages/dashboard.py")

st.title("🎮 CodeQuest")
st.subheader("📝 Criar nova conta")

with st.form("form_cadastro"):
    nome = st.text_input("👤 Nome")
    email = st.text_input("📧 Email")
    senha = st.text_input("🔒 Senha", type="password")
    confirmar = st.text_input("🔒 Confirmar senha", type="password")
    cadastrar = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)

if cadastrar:
    if not nome or not email or not senha or not confirmar:
        st.error("Preencha todos os campos.")
    elif senha != confirmar:
        st.error("As senhas não conferem.")
    elif len(senha) < 6:
        st.error("Senha deve ter ao menos 6 caracteres.")
    else:
        with st.spinner("Criando conta..."):
            user, erro = registrar_usuario(nome, email, senha)
        if erro:
            st.error(erro)
        else:
            st.success("✅ Conta criada! Verifique seu email para confirmar o cadastro, depois faça login.")
            st.switch_page("pages/login.py")

st.divider()
if st.button("← Voltar ao Login"):
    st.switch_page("pages/login.py")
