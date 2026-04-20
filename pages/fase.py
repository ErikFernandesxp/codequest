import streamlit as st
import json
from backend.validator import validar_codigo

# carregar fases
with open("data/fases.json") as f:
    fases = json.load(f)

# sessão
if "fase" not in st.session_state:
    st.session_state["fase"] = 0

linguagem = st.session_state.get("linguagem", "c")
fase_atual = st.session_state["fase"]

# valida existência da linguagem
if linguagem not in fases:
    st.error("❌ Linguagem não encontrada no sistema")
    st.stop()

# valida fim
if fase_atual >= len(fases[linguagem]):
    st.success("🎉 Parabéns! Você concluiu todas as fases!")
    st.button("🔄 Recomeçar", on_click=lambda: st.session_state.update({"fase": 0}))
    st.stop()

fase = fases[linguagem][fase_atual]

# progresso
progresso = (fase_atual + 1) / len(fases[linguagem])
st.progress(progresso)

# UI
st.title(f"📘 {fase['titulo']}")

st.markdown("### 📖 Explicação")
st.info(fase.get("explicacao", ""))

st.markdown("### 🧪 Exemplo")
st.code(fase.get("exemplo", ""), language=linguagem)

st.markdown("### 💡 Dica")
st.warning(fase.get("dica", ""))

st.markdown("### 🎯 Desafio")
st.write(fase.get("desafio", ""))

resposta = st.text_area("✍️ Digite seu código")

if st.button("🚀 Enviar resposta"):
    correto, feedback = validar_codigo(resposta, fase["resposta"])

    if correto:
        st.success(feedback)
        st.session_state["fase"] += 1
        st.rerun()
    else:
        st.error(feedback)
