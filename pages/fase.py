import streamlit as st
import json
from backend.validator import validar_codigo

# carregar JSON
with open("data/fases.json") as f:
    fases = json.load(f)

# inicializar sessão
if "fase" not in st.session_state:
    st.session_state["fase"] = 0

if "linguagem" not in st.session_state:
    st.session_state["linguagem"] = "python"

# pegar linguagem segura
linguagem = st.session_state["linguagem"].lower()
fase_atual = st.session_state["fase"]

# DEBUG (pode remover depois)
st.write("🔎 Linguagem atual:", linguagem)
st.write("📂 Linguagens disponíveis:", list(fases.keys()))

# valida linguagem
if linguagem not in fases:
    st.error(f"❌ Linguagem '{linguagem}' não encontrada no sistema")
    st.stop()

# valida fases vazias
if len(fases[linguagem]) == 0:
    st.error("❌ Essa linguagem ainda não tem fases cadastradas")
    st.stop()

# fim do jogo
if fase_atual >= len(fases[linguagem]):
    st.success("🎉 Parabéns! Você concluiu todas as fases!")
    if st.button("🔄 Reiniciar"):
        st.session_state["fase"] = 0
        st.rerun()
    st.stop()

fase = fases[linguagem][fase_atual]

# progresso
st.progress((fase_atual + 1) / len(fases[linguagem]))

# interface
st.title(f"📘 {fase.get('titulo', 'Sem título')}")

st.markdown("### 📖 Explicação")
st.info(fase.get("explicacao", ""))

st.markdown("### 🧪 Exemplo")
st.code(fase.get("exemplo", ""), language=linguagem)

st.markdown("### 💡 Dica")
st.warning(fase.get("dica", ""))

st.markdown("### 🎯 Desafio")
st.write(fase.get("desafio", ""))

resposta = st.text_area("✍️ Digite seu código")

# botão enviar
if st.button("🚀 Enviar resposta"):
    correto, feedback = validar_codigo(resposta, fase.get("resposta", ""))

    if correto:
        st.success(feedback)
        st.session_state["fase"] += 1
        st.rerun()
    else:
        st.error(feedback)
