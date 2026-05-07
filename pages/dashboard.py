import streamlit as st
import json, os

st.set_page_config(page_title="CodeQuest - Dashboard", page_icon="🎮", layout="wide")

from backend.session import init_session
from backend.crud import buscar_progresso, logout_usuario, atualizar_streak, calcular_vidas_regeneradas, atualizar_vidas, buscar_perfil, verificar_e_conceder_badges

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

user_id = st.session_state["user_id"]

# Busca perfil atualizado
perfil = buscar_perfil(user_id)
if perfil:
    # Atualiza streak
    novo_streak = atualizar_streak(user_id, perfil)
    st.session_state["streak"] = novo_streak

    # Regenera vidas
    vidas_novas = calcular_vidas_regeneradas(
        perfil.get("ultima_vida", ""),
        perfil.get("vidas", 3)
    )
    if vidas_novas != perfil.get("vidas", 3):
        atualizar_vidas(user_id, vidas_novas)
    st.session_state["vidas"] = vidas_novas
    st.session_state["xp"] = perfil.get("xp", 0)
    st.session_state["nivel"] = perfil.get("nivel", 1)
    st.session_state["usuario"] = perfil.get("nome", st.session_state["usuario"])

usuario = st.session_state["usuario"]
xp = st.session_state["xp"]
nivel = st.session_state["nivel"]
vidas = st.session_state.get("vidas", 3)
streak = st.session_state.get("streak", 0)

@st.cache_data
def carregar_fases():
    caminho = os.path.join(os.getcwd(), "data", "fases.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def carregar_badges_config():
    caminho = os.path.join(os.getcwd(), "data", "badges.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()
badges_config = carregar_badges_config()

progresso = buscar_progresso(user_id)
concluidas = {}
for p in progresso:
    lang = p["linguagem"]
    concluidas[lang] = concluidas.get(lang, 0) + 1

total_fases_concluidas = sum(concluidas.values())

# Verifica badges
novas_badges, _ = verificar_e_conceder_badges(
    user_id, perfil or {},
    total_fases_concluidas,
    fases_por_lang=concluidas
)
if novas_badges:
    for b in novas_badges:
        cfg = badges_config.get(b, {})
        st.toast(f"🏅 Badge conquistada: {cfg.get('emoji','')} {cfg.get('nome','')}", icon="🎉")

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {usuario}")
    st.metric("⚡ XP", xp)
    st.metric("🏆 Nível", nivel)
    st.progress(min((xp % 50) / 50, 1.0), text=f"XP para nível {nivel+1}: {xp % 50}/50")
    st.metric("❤️ Vidas", vidas)
    st.metric("🔥 Sequência de dias", f"{streak} dias seguidos")
    st.divider()
    if st.button("🏆 Ranking", use_container_width=True):
        st.switch_page("pages/ranking.py")
    if st.button("🚪 Sair", use_container_width=True):
        logout_usuario()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.switch_page("pages/login.py")

st.title("🎮 CodeQuest")
st.markdown(f"## Olá, **{usuario}**! Pronto para aprender? 🚀")

# Streak banner
if streak >= 3:
    st.success(f"🔥 Incrível! Você está jogando há **{streak} dias seguidos**! Não pare agora!")
elif streak == 2:
    st.info("🌱 Você jogou 2 dias seguidos! Volte amanhã para continuar a sequência!")
elif streak == 1:
    st.info("🌱 Primeiro dia! Volte amanhã para começar sua sequência de dias!")

st.divider()
st.subheader("📊 Seu Progresso")

lang_icons = {"python": "🐍", "c": "⚙️", "java": "☕", "php": "🌐"}
cols = st.columns(len(fases))
for i, (lang, fs) in enumerate(fases.items()):
    total = len(fs)
    feitas = concluidas.get(lang, 0)
    with cols[i]:
        st.metric(f"{lang_icons.get(lang,'')} {lang.upper()}", f"{feitas}/{total} fases")
        st.progress(feitas / total if total else 0)

st.divider()

# Badges
st.subheader("🏅 Suas Conquistas")
badges_usuario = perfil.get("badges", []) if perfil else []
if badges_usuario:
    cols_b = st.columns(6)
    for i, badge_key in enumerate(badges_usuario):
        cfg = badges_config.get(badge_key, {})
        with cols_b[i % 6]:
            st.markdown(f"### {cfg.get('emoji','🏅')}")
            st.caption(cfg.get("nome", badge_key))
else:
    st.caption("Nenhuma conquista ainda. Jogue para ganhar badges! 🎯")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📚 Escolher Linguagem", use_container_width=True, type="primary"):
        st.switch_page("pages/linguagem.py")
with col2:
    if st.session_state.get("linguagem") and st.button("🎯 Continuar", use_container_width=True):
        st.switch_page("pages/fase.py")
with col3:
    if st.button("🏆 Ver Ranking", use_container_width=True):
        st.switch_page("pages/ranking.py")
