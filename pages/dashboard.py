import streamlit as st

st.set_page_config(page_title="CodeQuest - Dashboard", page_icon="🎮", layout="wide")

from backend.session import init_session
from backend.crud import buscar_progresso, logout_usuario

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

usuario = st.session_state["usuario"]
xp = st.session_state["xp"]
nivel = st.session_state["nivel"]
user_id = st.session_state["user_id"]

with st.sidebar:
    st.markdown(f"### 👤 {usuario}")
    st.metric("⚡ XP", xp)
    st.metric("🏆 Nível", nivel)
    st.progress(min((xp % 50) / 50, 1.0), text=f"XP para nível {nivel+1}: {xp % 50}/50")
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

import json, os

@st.cache_data
def carregar_fases():
    caminho = os.path.join(os.getcwd(), "data", "fases.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()
progresso = buscar_progresso(user_id)
concluidas = {}
for p in progresso:
    lang = p["linguagem"]
    concluidas[lang] = concluidas.get(lang, 0) + 1

st.divider()
st.subheader("📊 Seu Progresso")

cols = st.columns(len(fases))
lang_icons = {"python": "🐍", "c": "⚙️", "java": "☕", "php": "🌐"}

for i, (lang, fs) in enumerate(fases.items()):
    total = len(fs)
    feitas = concluidas.get(lang, 0)
    with cols[i]:
        st.metric(f"{lang_icons.get(lang,'')} {lang.upper()}", f"{feitas}/{total} fases")
        st.progress(feitas / total if total else 0)

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
