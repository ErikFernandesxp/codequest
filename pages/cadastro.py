import streamlit as st
import re

st.set_page_config(page_title="CodeQuest", page_icon="🎮", layout="centered", initial_sidebar_state="collapsed")

from backend.session import init_session
from backend.crud import registrar_usuario

init_session(st)

if st.session_state.get("logado"):
    st.switch_page("pages/dashboard.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0f0f13; color: #f0efe8; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
div[data-testid="stTextInput"] input {
    background: #0f0f13 !important; color: #f0efe8 !important;
    border: 1px solid #2a2a35 !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
}
div[data-testid="stTextInput"] input:focus { border-color: #7c6af7 !important; }
div[data-testid="stTextInput"] label { color: #9b9ba8 !important; font-size: 0.8rem !important; }
.stButton button {
    border-radius: 12px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

def email_valido(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

col_c, col_m, col_c2 = st.columns([1, 2, 1])
with col_m:
    st.markdown("""
    <div style='text-align:center;margin:40px 0 32px;'>
        <div style='font-size:2rem;font-weight:800;letter-spacing:-1px;'>Code<span style="color:#7c6af7;">Quest</span></div>
        <div style='color:#9b9ba8;font-size:0.9rem;margin-top:6px;'>Crie sua conta grátis</div>
    </div>
    """, unsafe_allow_html=True)

    nome     = st.text_input("Nome completo", placeholder="Seu nome")
    email    = st.text_input("Email", placeholder="seu@email.com")
    senha    = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
    confirma = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    cadastrar = st.button("Criar conta →", use_container_width=True, type="primary")
    voltar    = st.button("← Já tenho conta", use_container_width=True)

if cadastrar:
    if not all([nome, email, senha, confirma]):
        st.error("Preencha todos os campos.")
    elif not email_valido(email):
        st.error("Email inválido. Ex: nome@gmail.com")
    elif senha != confirma:
        st.error("As senhas não conferem.")
    elif len(senha) < 6:
        st.error("Senha deve ter ao menos 6 caracteres.")
    else:
        with st.spinner("Criando conta..."):
            user, erro = registrar_usuario(nome, email, senha)
        if erro:
            st.error(erro)
        else:
            st.success("✅ Conta criada! Faça login para começar.")
            st.switch_page("pages/login.py")

if voltar:
    st.switch_page("pages/login.py")
