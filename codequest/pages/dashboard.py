import streamlit as st

st.title("Escolha sua linguagem")

linguagem = st.selectbox("Linguagem", ["Python", "C", "Java", "PHP"])

if st.button("Começar"):
    st.session_state["linguagem"] = linguagem
    st.switch_page("pages/fase.py")