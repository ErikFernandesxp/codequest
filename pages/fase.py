import streamlit as st
import json
from backend.validator import validar_codigo

with open("data/fases.json") as f:
    fases = json.load(f)

# sessão
if "fase" not in st.session_state:
    st.session_state["fase"] = 0

linguagem = st.session_state.get("linguagem", "c")
fase_atual = st.session_state["fase"]

if fase_atual >= len(fases[linguagem]):
    st.success("🎉 Você concluiu tudo!")
    st.stop()

fase = fases[linguagem][fase_atual]

# UI
st.title(f"📘 {fase['titulo']}")

# 📖 explicação
st.markdown("### 📖 Explicação")
st.info(fase["explicacao"])

# 🧪 exemplo
st.markdown("### 🧪 Exemplo")
st.code(fase["exemplo"], language=linguagem)

# 💡 dica
st.markdown("### 💡 Dica")
st.warning(fase["dica"])

# 🎯 desafio
st.markdown("### 🎯 Desafio")
st.write(fase["desafio"])

# input
resposta = st.text_area("✍️ Digite seu código aqui")

# botão
if st.button("🚀 Enviar resposta"):
    correto, feedback = validar_codigo(resposta, fase["resposta"])

    if correto:
        st.success("✅ " + feedback)
        st.session_state["fase"] += 1
        st.rerun()
    else:
        st.error("❌ " + feedback)
