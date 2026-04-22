import streamlit as st
import json
from backend.session import init_session
from backend.validator import validar_codigo

init_session(st)

@st.cache_data
def carregar_fases():
    with open("data/fases.json") as f:
        return json.load(f)

if not st.session_state["linguagem"]:
    st.switch_page("pages/linguagem.py")

fases = carregar_fases()
ling = st.session_state["linguagem"]
fase_atual = st.session_state["fase"]

# HUD
st.sidebar.metric("XP", st.session_state["xp"])
st.sidebar.metric("Nível", st.session_state["nivel"])
st.sidebar.metric("❤️ Vidas", st.session_state["vidas"])

if st.session_state["vidas"] <= 0:
    st.error("💀 Game Over")

    if st.button("🔄 Recomeçar"):
        st.session_state["vidas"] = 3
        st.session_state["fase"] = 0
        st.session_state["desafio_atual"] = 0
        st.rerun()

    st.stop()

fase = fases[ling][fase_atual]

desafios = fase["desafios"]
respostas = fase["respostas"]

idx = st.session_state["desafio_atual"]

st.title(f"🎯 Fase {fase_atual+1}")

st.write(fase["explicacao"])
st.code(fase["exemplo"], language=ling)

st.markdown(f"### Desafio {idx+1}")
st.write(desafios[idx])

resposta = st.text_area("Digite seu código")

if st.button("Enviar"):
    ok, feedback = validar_codigo(resposta, respostas[idx])

    if ok:
        st.success("✅ Acertou!")
        st.session_state["xp"] += 10
        st.session_state["desafio_atual"] += 1

        if st.session_state["desafio_atual"] >= len(desafios):
            st.success("🏆 Fase concluída!")
            st.session_state["fase"] += 1
            st.session_state["desafio_atual"] = 0

        st.rerun()

    else:
        st.session_state["vidas"] -= 1
        st.error("❌ Errou")
        st.info(feedback)
