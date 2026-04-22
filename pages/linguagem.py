import streamlit as st
from backend.session import init_session

init_session(st)

st.title("📚 Escolha sua Linguagem")

opcoes = {
    "Python 🐍": "python",
    "C ⚙️": "c",
    "Java ☕": "java",
    "PHP 🌐": "php"
}

ling = st.selectbox("Selecione:", list(opcoes.keys()))

if st.button("🚀 Começar"):
    st.session_state["linguagem"] = opcoes[ling]
    st.session_state["fase"] = 0
    st.switch_page("pages/fase.py")
