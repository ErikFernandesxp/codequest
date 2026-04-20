import streamlit as st
from backend.crud import criar_usuario

st.title("Login")

email = st.text_input("Digite seu email")

if st.button("Entrar"):
    criar_usuario(email)
    st.session_state["user"] = email
    st.success("Logado com sucesso!")