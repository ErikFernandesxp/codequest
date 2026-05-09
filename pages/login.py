import streamlit as st
st.set_page_config(page_title="CodeQuest", page_icon="🎮", layout="centered",
                   initial_sidebar_state="collapsed")

from backend.session import init_session, verificar_admin
from backend.crud import login_usuario, buscar_perfil
from backend.theme import CSS

init_session(st)

# ── Persistência de sessão via query_params ───────────────────────────────────
# Se já tem sessão ativa, vai direto pro dashboard
if st.session_state.get("logado"):
    st.switch_page("pages/dashboard.py")

# Tenta restaurar sessão salva nos query_params
params = st.query_params
if not st.session_state.get("logado") and "uid" in params:
    try:
        from backend.crud import buscar_perfil
        uid   = params["uid"]
        email = params.get("em", "")
        perfil = buscar_perfil(uid)
        if perfil:
            is_admin = verificar_admin(email)
            st.session_state.update({
                "logado":        True,
                "user_id":       uid,
                "usuario_email": email,
                "is_admin":      is_admin,
                "usuario":       perfil.get("nome", email.split("@")[0]),
                "xp":            perfil.get("xp", 0),
                "nivel":         perfil.get("nivel", 1),
                "vidas":         999 if is_admin else perfil.get("vidas", 3),
            })
            st.switch_page("pages/dashboard.py")
    except Exception:
        pass

st.markdown(CSS, unsafe_allow_html=True)
st.markdown("""
<style>
.login-card {
    background: #1c1f27;
    border: 1.5px solid #2e3240;
    border-radius: 20px;
    padding: 40px 36px 32px;
    max-width: 420px;
    margin: 48px auto 0;
}
.cq-logo {
    font-size: 2.2rem; font-weight: 800;
    letter-spacing: -1px; text-align: center;
    color: #f4f3ee;
}
.cq-logo span { color: #7c6af7; }
.cq-tagline {
    text-align: center; color: #b0b3c1;
    font-size: 0.92rem; margin: 6px 0 32px;
}
.cq-hint {
    text-align: center; color: #7a7d8e;
    font-size: 0.75rem; margin-top: 20px;
    letter-spacing: 0.3px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="login-card">
  <div class="cq-logo">Code<span>Quest</span></div>
  <div class="cq-tagline">🎮 Aprenda programação jogando</div>
</div>
""", unsafe_allow_html=True)

_, col, _ = st.columns([1, 10, 1])
with col:
    email  = st.text_input("Email", placeholder="seu@email.com")
    senha  = st.text_input("Senha", type="password", placeholder="••••••••")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    entrar = st.button("Entrar →", use_container_width=True, type="primary")
    criar  = st.button("Criar conta grátis", use_container_width=True)
    st.markdown('<p class="cq-hint">Python · C · Java · PHP</p>', unsafe_allow_html=True)

if entrar:
    if not email or not senha:
        st.error("Preencha email e senha.")
    else:
        with st.spinner("Verificando..."):
            user, session, erro = login_usuario(email, senha)
        if erro == "email_nao_encontrado":
            st.error("❌ Email não cadastrado. Crie uma conta primeiro.")
        elif erro == "senha_incorreta":
            st.error("❌ Senha incorreta.")
        elif erro:
            st.error(f"❌ {erro}")
        else:
            is_admin = verificar_admin(email)
            perfil   = buscar_perfil(user.id)
            nome     = (user.user_metadata or {}).get("nome", email.split("@")[0])
            st.session_state.update({
                "logado":        True,
                "user_id":       user.id,
                "usuario_email": email,
                "is_admin":      is_admin,
                "usuario":       perfil.get("nome", nome) if perfil else nome,
                "xp":            perfil.get("xp", 0)      if perfil else 0,
                "nivel":         perfil.get("nivel", 1)    if perfil else 1,
                "vidas":         999 if is_admin else (perfil.get("vidas", 3) if perfil else 3),
            })
            # Salva uid e email nos query_params para persistir ao recarregar
            st.query_params["uid"] = user.id
            st.query_params["em"]  = email
            st.switch_page("pages/dashboard.py")

if criar:
    st.switch_page("pages/cadastro.py")
