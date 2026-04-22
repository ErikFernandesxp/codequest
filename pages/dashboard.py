import streamlit as st
from backend.session import init_session

init_session(st)

if not st.session_state["logado"]:
    st.switch_page("pages/login.py")

st.title("🎮 CodeQuest")

st.sidebar.metric("XP", st.session_state["xp"])
st.sidebar.metric("Nível", st.session_state["nivel"])

st.markdown("""
## 🚀 Bem-vindo ao CodeQuest

Aprenda programação jogando 🎮
""")

if st.button("📚 Escolher Linguagem"):
    st.switch_page("pages/linguagem.py")

if st.button("🎯 Continuar"):
    st.switch_page("pages/fase.py")
