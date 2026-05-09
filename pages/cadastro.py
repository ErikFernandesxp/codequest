import streamlit as st

st.set_page_config(page_title="CodeQuest — Cadastro", page_icon="🎮",
                   layout="centered", initial_sidebar_state="collapsed")

import re
from backend.session import init_session
from backend.crud import registrar_usuario
from backend.theme import CSS

init_session(st)

if st.session_state.get("logado"):
    st.switch_page("pages/dashboard.py")

st.markdown(CSS, unsafe_allow_html=True)
st.markdown("""
<style>
.cq-logo { font-size:2rem; font-weight:800; letter-spacing:-1px;
           text-align:center; color:#f4f3ee; }
.cq-logo span { color:#7c6af7; }
.cq-tagline { text-align:center; color:#b0b3c1; font-size:0.9rem;
              margin:6px 0 28px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin:48px 0 24px;">
  <div class="cq-logo">Code<span>Quest</span></div>
  <div class="cq-tagline">Crie sua conta gratuita</div>
</div>
""", unsafe_allow_html=True)

_, col, _ = st.columns([1, 10, 1])
with col:
    nome     = st.text_input("Nome completo", placeholder="Seu nome")
    email    = st.text_input("Email", placeholder="seu@email.com")
    senha    = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")
    confirma = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    cadastrar = st.button("Criar conta →", use_container_width=True, type="primary")
    voltar    = st.button("← Já tenho conta", use_container_width=True)

def email_valido(e):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', e)

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
