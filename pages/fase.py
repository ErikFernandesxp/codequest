import streamlit as st
import json
import os
from backend.session import init_session
from backend.validator import validar_codigo

st.set_page_config(layout="wide")

init_session(st)

# 🔥 carregar JSON seguro
@st.cache_data
def carregar_fases():
    caminho = os.path.join(os.getcwd(), "data", "fases.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()

ling = st.session_state.get("linguagem")
fase_idx = st.session_state.get("fase", 0)

# 🔐 valida linguagem
if not ling or ling not in fases:
    st.error("Linguagem inválida")
    st.stop()

# 🔐 valida fase
if fase_idx >= len(fases[ling]):
    st.success("Você finalizou o jogo!")
    st.stop()

fase = fases[ling][fase_idx]

# 🔐 valida estrutura da fase
if not isinstance(fase, dict):
    st.error("Fase inválida no JSON")
    st.stop()

desafios = fase.get("desafios")
respostas = fase.get("respostas")

if not desafios or not respostas:
    st.error("Erro no JSON: fase sem desafios/respostas")
    st.stop()

idx = st.session_state.get("desafio_atual", 0)

if idx >= len(desafios):
    st.session_state["desafio_atual"] = 0
    st.rerun()

# 🎮 HUD
st.sidebar.metric("XP", st.session_state["xp"])
st.sidebar.metric("Nível", st.session_state["nivel"])
st.sidebar.metric("Vidas", st.session_state["vidas"])

# 💀 Game Over
if st.session_state["vidas"] <= 0:
    st.error("Game Over")

    if st.button("Recomeçar"):
        st.session_state["vidas"] = 3
        st.session_state["fase"] = 0
        st.session_state["desafio_atual"] = 0
        st.rerun()

    st.stop()

# 🎯 UI
st.title(f"Fase {fase_idx + 1} - {fase.get('titulo','')}")

st.write(fase.get("explicacao",""))
st.code(fase.get("exemplo",""), language=ling)

st.progress((idx + 1) / len(desafios))

st.write(desafios[idx])

resposta = st.text_area("Digite seu código")

# 🚀 lógica
if st.button("Enviar"):
    ok, feedback = validar_codigo(resposta, respostas[idx])

    if ok:
        st.success("Acertou!")
        st.session_state["xp"] += 10
        st.session_state["desafio_atual"] += 1

        if st.session_state["desafio_atual"] >= len(desafios):
            st.success("Fase concluída!")
            st.session_state["fase"] += 1
            st.session_state["desafio_atual"] = 0

        st.rerun()

    else:
        st.session_state["vidas"] -= 1
        st.error("Errou")
        st.info(feedback)
