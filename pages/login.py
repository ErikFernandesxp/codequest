import streamlit as st

st.set_page_config(page_title="CodeQuest - Login", page_icon="🔐", layout="centered")

from backend.session import init_session, verificar_admin
from backend.crud import login_usuario, buscar_perfil

init_session(st)

if st.session_state.get("logado"):
    st.switch_page("pages/dashboard.py")

st.title("🎮 CodeQuest")
st.subheader("🔐 Entrar na sua conta")

with st.form("form_login"):
    email = st.text_input("📧 Email")
    senha = st.text_input("🔒 Senha", type="password")
    col1, col2 = st.columns(2)
    entrar = col1.form_submit_button("Entrar", use_container_width=True, type="primary")
    criar = col2.form_submit_button("Criar Conta", use_container_width=True)

if entrar:
    if not email or not senha:
        st.error("Preencha todos os campos.")
    else:
        with st.spinner("Verificando..."):
            user, session, erro = login_usuario(email, senha)

        if erro == "email_nao_encontrado":
            st.error("❌ Este email não está cadastrado. Crie uma conta primeiro.")
        elif erro == "senha_incorreta":
            st.error("❌ Email ou senha incorretos.")
        elif erro:
            st.error(f"❌ {erro}")
        else:
            is_admin = verificar_admin(email)
            st.session_state["logado"] = True
            st.session_state["user_id"] = user.id
            st.session_state["usuario_email"] = email
            st.session_state["is_admin"] = is_admin
            nome = (user.user_metadata or {}).get("nome", email.split("@")[0])
            st.session_state["usuario"] = nome
            st.session_state["xp"] = 0
            st.session_state["nivel"] = 1
            st.session_state["vidas"] = 999 if is_admin else 3
            perfil = buscar_perfil(user.id)
            if perfil:
                st.session_state["xp"] = perfil.get("xp", 0)
                st.session_state["nivel"] = perfil.get("nivel", 1)
                st.session_state["usuario"] = perfil.get("nome", nome)
                if not is_admin:
                    st.session_state["vidas"] = perfil.get("vidas", 3)
            if is_admin:
                st.success(f"Bem-vindo, Admin {st.session_state['usuario']}! 👑")
            else:
                st.success(f"Bem-vindo, {st.session_state['usuario']}! 🚀")
            st.switch_page("pages/dashboard.py")

if criar:
    st.switch_page("pages/cadastro.py")
