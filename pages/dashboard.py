import streamlit as st

if not st.session_state.get("logado"):
    st.switch_page("login")

st.title("🎮 CodeQuest")

st.sidebar.metric("XP", st.session_state.get("xp", 0))
st.sidebar.metric("Nível", st.session_state.get("nivel", 1))

st.markdown("""
## 🚀 Bem-vindo

- Escolha uma linguagem
- Complete desafios
- Ganhe XP e evolua
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("📚 Escolher Linguagem"):
        st.switch_page("linguagem")

with col2:
    if st.button("🎯 Continuar"):
        st.switch_page("fase")
