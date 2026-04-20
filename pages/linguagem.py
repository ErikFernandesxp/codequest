import streamlit as st

st.title("📚 Escolha sua Linguagem")

opcoes = {
    "Python": "python",
    "C": "c",
    "Java": "java",
    "PHP": "php"
}

linguagem_nome = st.selectbox(
    "Selecione a linguagem que deseja aprender:",
    list(opcoes.keys())
)

if st.button("Confirmar"):
    # salva SEMPRE em minúsculo
    st.session_state["linguagem"] = opcoes[linguagem_nome].lower()
    st.session_state["fase"] = 0

    st.success(f"Você escolheu {linguagem_nome} 🚀")
    st.switch_page("fase")
