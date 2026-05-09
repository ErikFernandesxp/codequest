import streamlit as st

st.set_page_config(page_title="CodeQuest", page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

import json, os
from backend.session import init_session
from backend.crud import buscar_progresso, logout_usuario, atualizar_streak, calcular_vidas_regeneradas, atualizar_vidas, buscar_perfil, verificar_e_conceder_badges

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0f0f13; color: #f0efe8; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 28px; background: #16161d;
    border-bottom: 1px solid #2a2a35; margin-bottom: 32px;
    border-radius: 0 0 16px 16px;
}
.nav-logo { font-size: 1.4rem; font-weight: 800; letter-spacing: -0.5px; }
.nav-logo span { color: #7c6af7; }
.nav-user { display: flex; align-items: center; gap: 12px; }
.nav-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: linear-gradient(135deg, #7c6af7, #a78bfa);
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem; color: white;
}

.hero {
    background: linear-gradient(135deg, #1a1a24 0%, #16161d 100%);
    border: 1px solid #2a2a35; border-radius: 20px;
    padding: 32px 36px; margin-bottom: 28px;
    display: flex; align-items: center; justify-content: space-between;
}
.hero-greeting { font-size: 0.85rem; color: #7c6af7; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.hero-name { font-size: 2rem; font-weight: 800; color: #f0efe8; }
.hero-stats { display: flex; gap: 20px; }
.hero-stat {
    background: #0f0f13; border: 1px solid #2a2a35;
    border-radius: 12px; padding: 12px 20px; text-align: center; min-width: 80px;
}
.hero-stat-val { font-size: 1.4rem; font-weight: 800; color: #f0efe8; }
.hero-stat-lbl { font-size: 0.7rem; color: #9b9ba8; text-transform: uppercase; letter-spacing: 0.5px; }

.xp-bar-wrap { margin-top: 14px; }
.xp-bar-label { font-size: 0.75rem; color: #9b9ba8; margin-bottom: 6px; }
.xp-bar-bg { background: #2a2a35; border-radius: 4px; height: 8px; }
.xp-bar-fill { background: linear-gradient(90deg,#7c6af7,#a78bfa); height: 8px; border-radius: 4px; }

.section-title {
    font-size: 0.75rem; color: #9b9ba8; text-transform: uppercase;
    letter-spacing: 1.5px; font-weight: 700; margin: 28px 0 14px 0;
}

.lang-card {
    background: #16161d; border: 1px solid #2a2a35;
    border-radius: 16px; padding: 22px; transition: border-color 0.2s;
    height: 100%;
}
.lang-card:hover { border-color: #7c6af7; }
.lang-icon { font-size: 2rem; margin-bottom: 10px; }
.lang-name { font-size: 1rem; font-weight: 700; color: #f0efe8; }
.lang-prog { font-size: 0.8rem; color: #9b9ba8; margin: 4px 0 10px 0; }
.lang-bar-bg { background: #2a2a35; border-radius: 3px; height: 4px; }
.lang-bar-fill { background: linear-gradient(90deg,#7c6af7,#a78bfa); height: 4px; border-radius: 3px; }

.badge-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: #1e1e28; border: 1px solid #2a2a35;
    border-radius: 20px; padding: 6px 14px; margin: 4px;
    font-size: 0.82rem; color: #d4d3cc;
}

.btn-primary button {
    background: linear-gradient(135deg,#7c6af7,#a78bfa) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-family: 'Syne',sans-serif !important; font-size: 0.95rem !important;
}
.btn-secondary button {
    background: #1e1e28 !important; color: #d4d3cc !important;
    border: 1px solid #2a2a35 !important; border-radius: 12px !important;
    font-family: 'Syne',sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

user_id = st.session_state["user_id"]
perfil = buscar_perfil(user_id)
if perfil:
    novo_streak = atualizar_streak(user_id, perfil)
    st.session_state["streak"] = novo_streak
    if not st.session_state.get("is_admin"):
        vidas_novas = calcular_vidas_regeneradas(perfil.get("ultima_vida",""), perfil.get("vidas",3))
        if vidas_novas != perfil.get("vidas",3):
            atualizar_vidas(user_id, vidas_novas)
        st.session_state["vidas"] = vidas_novas
    st.session_state.update({
        "xp": perfil.get("xp",0),
        "nivel": perfil.get("nivel",1),
        "usuario": perfil.get("nome", st.session_state["usuario"])
    })

usuario = st.session_state["usuario"]
xp = st.session_state["xp"]
nivel = st.session_state["nivel"]
streak = st.session_state.get("streak",0)
is_admin = st.session_state.get("is_admin",False)
vidas = "∞" if is_admin else st.session_state.get("vidas",3)
xp_mod = xp % 50

@st.cache_data
def carregar_fases():
    with open(os.path.join(os.getcwd(),"data","fases.json"), encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def carregar_badges_config():
    with open(os.path.join(os.getcwd(),"data","badges.json"), encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()
badges_config = carregar_badges_config()
progresso = buscar_progresso(user_id)
concluidas = {}
for p in progresso:
    lang = p["linguagem"]
    concluidas[lang] = concluidas.get(lang,0) + 1

total_concluidas = sum(concluidas.values())
novas_badges, _ = verificar_e_conceder_badges(user_id, perfil or {}, total_concluidas, fases_por_lang=concluidas)
for b in novas_badges:
    cfg = badges_config.get(b,{})
    st.toast(f"🏅 {cfg.get('emoji','')} {cfg.get('nome','')}", icon="🎉")

inicial = usuario[0].upper() if usuario else "?"

# ─── Navbar ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
    <div class="nav-logo">Code<span>Quest</span></div>
    <div class="nav-user">
        {'<span style="background:#7c6af7;color:white;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">👑 ADMIN</span>' if is_admin else ''}
        <div class="nav-avatar">{inicial}</div>
        <span style="font-weight:600;color:#f0efe8;">{usuario}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div style="flex:1;">
        <div class="hero-greeting">{"👑 Modo Admin" if is_admin else "Bem-vindo de volta"}</div>
        <div class="hero-name">{usuario}</div>
        {'<div style="color:#fbbf24;font-size:0.85rem;margin-top:4px;">🔥 '+str(streak)+' dias seguidos!</div>' if streak >= 2 else ''}
        <div class="xp-bar-wrap">
            <div class="xp-bar-label">Nível {nivel} → {nivel+1} &nbsp;·&nbsp; {xp_mod}/50 XP</div>
            <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{min(xp_mod/50*100,100):.0f}%"></div></div>
        </div>
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-val">{xp}</div>
            <div class="hero-stat-lbl">XP</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val">{nivel}</div>
            <div class="hero-stat-lbl">Nível</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val">{vidas}</div>
            <div class="hero-stat-lbl">Vidas</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-val">{streak}</div>
            <div class="hero-stat-lbl">Dias</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Botões de ação ──────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("🚀 Escolher Linguagem e Jogar", use_container_width=True):
        st.switch_page("pages/linguagem.py")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("🏆 Ranking", use_container_width=True):
        st.switch_page("pages/ranking.py")
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("🚪 Sair", use_container_width=True):
        logout_usuario()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.switch_page("pages/login.py")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Progresso por linguagem ─────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Suas Trilhas</div>', unsafe_allow_html=True)
lang_data = [
    ("python","🐍","Python"),
    ("c","⚙️","C"),
    ("java","☕","Java"),
    ("php","🌐","PHP")
]
cols = st.columns(4)
for i, (lang, icon, label) in enumerate(lang_data):
    total = len(fases.get(lang,[]))
    feitas = concluidas.get(lang,0)
    pct = int(feitas/total*100) if total else 0
    with cols[i]:
        st.markdown(f"""
        <div class="lang-card">
            <div class="lang-icon">{icon}</div>
            <div class="lang-name">{label}</div>
            <div class="lang-prog">{feitas}/{total} fases · {pct}%</div>
            <div class="lang-bar-bg"><div class="lang-bar-fill" style="width:{pct}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

# ─── Badges ──────────────────────────────────────────────────────────────────
badges_usuario = perfil.get("badges",[]) if perfil else []
st.markdown('<div class="section-title">🏅 Conquistas</div>', unsafe_allow_html=True)
if badges_usuario:
    badges_html = "".join([
        f'<div class="badge-chip">{badges_config.get(b,{}).get("emoji","🏅")} {badges_config.get(b,{}).get("nome",b)}</div>'
        for b in badges_usuario
    ])
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:4px;">{badges_html}</div>', unsafe_allow_html=True)
else:
    st.markdown('<p style="color:#9b9ba8;font-size:0.9rem;">Nenhuma conquista ainda. Jogue para ganhar badges! 🎯</p>', unsafe_allow_html=True)
