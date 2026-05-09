import streamlit as st

st.set_page_config(page_title="CodeQuest", page_icon="🎮", layout="centered", initial_sidebar_state="collapsed")

from backend.session import init_session, verificar_admin
from backend.crud import login_usuario, buscar_perfil

init_session(st)

if st.session_state.get("logado"):
    st.switch_page("pages/dashboard.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0f0f13; color: #f0efe8; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.login-wrap {
    max-width: 420px; margin: 60px auto 0;
    background: #16161d; border: 1px solid #2a2a35;
    border-radius: 24px; padding: 40px 36px;
}
.login-logo {
    font-size: 2rem; font-weight: 800; text-align: center;
    margin-bottom: 4px; letter-spacing: -1px;
}
.login-logo span { color: #7c6af7; }
.login-sub { text-align: center; color: #9b9ba8; font-size: 0.9rem; margin-bottom: 32px; }

div[data-testid="stTextInput"] input {
    background: #0f0f13 !important; color: #f0efe8 !important;
    border: 1px solid #2a2a35 !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important; font-size: 0.95rem !important;
    padding: 12px 16px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.2) !important;
}
div[data-testid="stTextInput"] label { color: #9b9ba8 !important; font-size: 0.8rem !important; }

.stButton button {
    border-radius: 12px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    padding: 10px !important; transition: all 0.2s !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="login-wrap">
    <div class="login-logo">Code<span>Quest</span></div>
    <div class="login-sub">Aprenda programação jogando 🎮</div>
</div>
""", unsafe_allow_html=True)

col_c, col_m, col_c2 = st.columns([1, 2, 1])
with col_m:
    email = st.text_input("Email", placeholder="seu@email.com")
    senha = st.text_input("Senha", type="password", placeholder="••••••••")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    entrar = st.button("Entrar →", use_container_width=True, type="primary")
    criar  = st.button("Criar conta grátis", use_container_width=True)

    st.markdown("<div style='text-align:center;margin-top:16px;color:#9b9ba8;font-size:0.75rem;'>Aprenda Python, C, Java e PHP</div>", unsafe_allow_html=True)

if entrar:
    if not email or not senha:
        st.error("Preencha todos os campos.")
    else:
        with st.spinner("Verificando..."):
            user, session, erro = login_usuario(email, senha)
        if erro == "email_nao_encontrado":
            st.error("❌ Email não cadastrado. Crie uma conta primeiro.")
        elif erro == "senha_incorreta":
            st.error("❌ Email ou senha incorretos.")
        elif erro:
            st.error(f"❌ {erro}")
        else:
            is_admin = verificar_admin(email)
            perfil = buscar_perfil(user.id)
            nome = (user.user_metadata or {}).get("nome", email.split("@")[0])
            st.session_state.update({
                "logado": True,
                "user_id": user.id,
                "usuario_email": email,
                "is_admin": is_admin,
                "usuario": perfil.get("nome", nome) if perfil else nome,
                "xp": perfil.get("xp", 0) if perfil else 0,
                "nivel": perfil.get("nivel", 1) if perfil else 1,
                "vidas": 999 if is_admin else (perfil.get("vidas", 3) if perfil else 3),
            })
            st.switch_page("pages/dashboard.py")

if criar:
    st.switch_page("pages/cadastro.py")
