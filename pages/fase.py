import streamlit as st
import json
from backend.session import init_session
from backend.validator import validar_codigo
from backend.memory import limpar_memoria

init_session(st)

@st.cache_data
def carregar_fases():
    with open("data/fases.json") as f:
        return json.load(f)

# proteção
if not st.session_state["linguagem"]:
    st.switch_page("pages/linguagem.py")

fases = carregar_fases()

ling = st.session_state["linguagem"]
fase_atual = st.session_state["fase"]

st.sidebar.metric("XP", st.session_state["xp"])
st.sidebar.metric("Nível", st.session_state["nivel"])

# erro de linguagem
if ling not in fases:
    st.error("Linguagem inválida")
    st.stop()

# fim do jogo
if fase_atual >= len(fases[ling]):
    st.success("🎉 Você concluiu tudo!")

    if st.button("Reiniciar"):
        st.session_state["fase"] = 0
        st.rerun()

    st.stop()

fase = fases[ling][fase_atual]

st.progress((fase_atual + 1) / len(fases[ling]))

st.title(f"🎯 Fase {fase_atual+1} - {fase['titulo']}")

col1, col2 = st.columns(2)

with col1:
    st.info(fase["explicacao"])
    st.warning("💡 " + fase["dica"])

with col2:
    st.code(fase["exemplo"], language=ling)

st.markdown("### 🎯 Desafio")
st.write(fase["desafio"])

resposta = st.text_area("💻 Digite seu código")

if st.button("🚀 Enviar"):
    correto, feedback = validar_codigo(resposta, fase["resposta"])

    if correto:
        st.success(feedback)

        st.session_state["xp"] += 10

        if st.session_state["xp"] >= st.session_state["nivel"] * 50:
            st.session_state["nivel"] += 1
            st.toast("⬆️ Subiu de nível!")

        st.session_state["fase"] += 1

        limpar_memoria()
        st.rerun()

    else:
        st.error("❌ Código incorreto")
        st.markdown("### 🧑‍🏫 Professor")
        st.info(feedback)
