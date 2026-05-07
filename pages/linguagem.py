import streamlit as st

st.set_page_config(page_title="CodeQuest - Linguagem", page_icon="🧩", layout="centered")

from backend.session import init_session
from backend.crud import buscar_progresso

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

import json, os

@st.cache_data
def carregar_fases():
    caminho = os.path.join(os.getcwd(), "data", "fases.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()

st.title("🎮 CodeQuest")
st.subheader("Escolha sua linguagem de programação")

opcoes = {
    "Python 🐍": "python",
    "C ⚙️": "c",
    "Java ☕": "java",
    "PHP 🌐": "php"
}

progresso = buscar_progresso(st.session_state["user_id"])
concluidas = {}
for p in progresso:
    lang = p["linguagem"]
    concluidas[lang] = concluidas.get(lang, 0) + 1

ling_label = st.selectbox("Selecione a linguagem:", list(opcoes.keys()))
linguagem = opcoes[ling_label]

total_fases = len(fases.get(linguagem, []))
feitas = concluidas.get(linguagem, 0)

st.info(f"📊 Progresso em {linguagem.upper()}: **{feitas}/{total_fases}** fases concluídas")

# Calcula a próxima fase não concluída
fases_feitas_set = {p["fase"] for p in progresso if p["linguagem"] == linguagem}
proxima_fase = 0
for i in range(total_fases):
    if i not in fases_feitas_set:
        proxima_fase = i
        break
else:
    proxima_fase = total_fases  # já terminou tudo

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Começar do início", use_container_width=True):
        st.session_state["linguagem"] = linguagem
        st.session_state["fase"] = 0
        st.session_state["desafio_atual"] = 0
        st.session_state["vidas"] = 3
        st.switch_page("pages/fase.py")

with col2:
    if feitas > 0 and st.button("▶️ Continuar", use_container_width=True, type="primary"):
        st.session_state["linguagem"] = linguagem
        st.session_state["fase"] = proxima_fase
        st.session_state["desafio_atual"] = 0
        st.session_state["vidas"] = 3
        st.switch_page("pages/fase.py")

st.divider()
if st.button("← Voltar ao Dashboard"):
    st.switch_page("pages/dashboard.py")
