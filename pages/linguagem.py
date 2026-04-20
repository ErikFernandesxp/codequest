import streamlit as st

st.title("📚 Escolha sua Linguagem")

linguagem = st.selectbox(
    "Selecione a linguagem que deseja aprender:",
    ["Python", "C", "Java", "PHP"]
)

if st.button("Confirmar"):
    st.session_state["linguagem"] = linguagem
    st.session_state["fase"] = 0
    st.success(f"Você escolheu {linguagem} 🚀")
    st.switch_page("pages/fase.py")