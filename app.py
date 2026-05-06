import streamlit as st

st.set_page_config(page_title="CodeQuest", page_icon="🎮", layout="wide")

from backend.session import init_session

init_session(st)

# Redireciona automaticamente baseado no estado de login
if st.session_state["logado"]:
    st.switch_page("pages/dashboard.py")
else:
    st.switch_page("pages/login.py")
