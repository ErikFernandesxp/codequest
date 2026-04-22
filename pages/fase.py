import streamlit as st
import json
from backend.session import init_session
from backend.validator import validar_codigo

st.set_page_config(layout="wide")

init_session(st)

@st.cache_data
def carregar_fases():
    with open("data/fases.json") as f:
        return json.load(f)

# 🔐 proteção
if not st.session_state.get("linguagem"):
    st.switch_page("pages/linguagem.py")

fases = carregar_fases()
ling = st.session_state["linguagem"]
fase_atual = st.session_state["fase"]

# 🧠 valida linguagem
if ling not in fases:
    st.error("❌ Linguagem não encontrada no JSON")
    st.stop()

# 🧠 valida fase
if fase_atual >= len(fases[ling]):
    st.success("🎉 Você finalizou o jogo!")

    if st.button("🔄 Recomeçar"):
        st.session_state["fase"] = 0
        st.session_state["desafio_atual"] = 0
        st.session_state["vidas"] = 3
        st.rerun()

    st.stop()

fase = fases[ling][fase_atual]

# 🔥 proteção contra JSON incompleto
if "desafios" not in fase or "respostas" not in fase:
    st.error("⚠️ Erro no JSON: fase sem desafios/respostas")
    st.stop()

desafios = fase["desafios"]
respostas = fase["respostas"]

# 🧠 índice seguro
idx = st.session_state.get("desafio_atual", 0)

if idx >= len(desafios):
    st.session_state["desafio_atual"] = 0
    st.rerun()

# 🎮 HUD
st.sidebar.metric("XP", st.session_state["xp"])
st.sidebar.metric("Nível", st.session_state["nivel"])
st.sidebar.metric("❤️ Vidas", st.session_state["vidas"])

# 💀 game over
if st.session_state["vidas"] <= 0:
    st.error("💀 Game Over")

    if st.button("🔄 Recomeçar"):
        st.session_state["vidas"] = 3
        st.session_state["fase"] = 0
        st.session_state["desafio_atual"] = 0
        st.rerun()

    st.stop()

# 🎯 progresso geral
st.progress((fase_atual + 1) / len(fases[ling]))

# 🎯 UI principal
st.title(f"🎯 Fase {fase_atual+1} - {fase.get('titulo', '')}")

col1, col2 = st.columns(2)

with col1:
    st.info(fase.get("explicacao", ""))
    st.warning("💡 " + fase.get("dica", "Use a lógica correta"))

with col2:
    st.code(fase.get("exemplo", ""), language=ling)

# 🎯 progresso da fase
st.markdown(f"### 🧩 Desafio {idx+1} de {len(desafios)}")
st.progress((idx + 1) / len(desafios))

st.write(desafios[idx])

resposta = st.text_area("💻 Digite seu código", key=f"input_{idx}")

# 🚀 ação
if st.button("Enviar"):
    ok, feedback = validar_codigo(resposta, respostas[idx])

    if ok:
        st.success("✅ Acertou!")

        st.session_state["xp"] += 10
        st.session_state["desafio_atual"] += 1

        # 🏆 terminou fase
        if st.session_state["desafio_atual"] >= len(desafios):
            st.success("🏆 Fase concluída!")

            st.session_state["fase"] += 1
            st.session_state["desafio_atual"] = 0

            # ⬆️ level up
            if st.session_state["xp"] >= st.session_state["nivel"] * 50:
                st.session_state["nivel"] += 1
                st.toast("⬆️ Subiu de nível!")

        st.rerun()

    else:
        st.session_state["vidas"] -= 1
        st.error("❌ Errou")
        st.markdown("### 🧑‍🏫 Professor")
        st.info(feedback)
