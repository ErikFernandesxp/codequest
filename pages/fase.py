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

# estado da fase (controle interno)
if "desafio_atual" not in st.session_state:
    st.session_state["desafio_atual"] = 0

if "acertos_fase" not in st.session_state:
    st.session_state["acertos_fase"] = 0

st.sidebar.metric("XP", st.session_state["xp"])
st.sidebar.metric("Nível", st.session_state["nivel"])

if ling not in fases:
    st.error("Linguagem inválida")
    st.stop()

# fim do jogo
if fase_atual >= len(fases[ling]):
    st.success("🎉 Você zerou o jogo!")

    if st.button("🔄 Reiniciar"):
        st.session_state["fase"] = 0
        st.session_state["desafio_atual"] = 0
        st.session_state["acertos_fase"] = 0
        st.rerun()

    st.stop()

fase = fases[ling][fase_atual]

desafio_idx = st.session_state["desafio_atual"]

# progresso geral
st.progress((fase_atual + 1) / len(fases[ling]))

st.title(f"🎯 Fase {fase_atual+1} - {fase['titulo']}")

# UI
col1, col2 = st.columns(2)

with col1:
    st.info(fase["explicacao"])
    st.warning("💡 " + fase["dica"])

with col2:
    st.code(fase["exemplo"], language=ling)

# progresso da fase
st.markdown(f"### 🧩 Desafio {desafio_idx+1} de {len(fase['desafios'])}")

st.progress((desafio_idx + 1) / len(fase["desafios"]))

st.write(fase["desafios"][desafio_idx])

resposta = st.text_area("💻 Seu código", key=f"input_{desafio_idx}")

if st.button("🚀 Enviar"):
    correto, feedback = validar_codigo(
        resposta,
        fase["respostas"][desafio_idx]
    )

    if correto:
        st.success("✅ Correto!")

        # XP por questão
        st.session_state["xp"] += 5

        st.session_state["acertos_fase"] += 1
        st.session_state["desafio_atual"] += 1

        limpar_memoria()

        # terminou fase
        if st.session_state["desafio_atual"] >= len(fase["desafios"]):
            st.success("🏆 Fase concluída!")

            st.session_state["fase"] += 1
            st.session_state["desafio_atual"] = 0
            st.session_state["acertos_fase"] = 0

            # LEVEL UP
            if st.session_state["xp"] >= st.session_state["nivel"] * 50:
                st.session_state["nivel"] += 1
                st.toast("⬆️ Subiu de nível!")

        st.rerun()

    else:
        st.error("❌ Incorreto")
        st.markdown("### 🧑‍🏫 Professor")
        st.info(feedback)
