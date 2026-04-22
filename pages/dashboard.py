import streamlit as st

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

st.title("🎮 CodeQuest")

st.sidebar.metric("XP", st.session_state.get("xp", 0))
st.sidebar.metric("Nível", st.session_state.get("nivel", 1))

st.markdown("""
## 🚀 Bem-vindo

Escolha uma linguagem e comece a evoluir.
""")

if st.button("📚 Escolher Linguagem"):
    st.switch_page("pages/linguagem.py")

if st.button("🎯 Continuar"):
    st.switch_page("pages/fase.py")
