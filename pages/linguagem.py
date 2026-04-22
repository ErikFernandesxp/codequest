import streamlit as st
from backend.session import init_session

st.set_page_config(layout="centered")

init_session(st)

st.title("🎮 CodeQuest")
st.subheader("Escolha sua linguagem")

opcoes = {
    "Python 🐍": "python",
    "C ⚙️": "c",
    "Java ☕": "java",
    "PHP 🌐": "php"
}

ling_label = st.selectbox("Selecione:", list(opcoes.keys()))

if st.button("Começar"):
    linguagem = opcoes[ling_label]

    st.session_state["linguagem"] = linguagem
    st.session_state["fase"] = 0
    st.session_state["desafio_atual"] = 0
    st.session_state["xp"] = 0
    st.session_state["nivel"] = 1
    st.session_state["vidas"] = 3

    st.switch_page("pages/fase.py")
