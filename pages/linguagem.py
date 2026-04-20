import streamlit as st

st.title("📚 Escolha sua Linguagem")

# Mapeamento correto (visual → sistema)
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
    st.session_state["linguagem"] = opcoes[linguagem_nome]  # 🔥 corrigido
    st.session_state["fase"] = 0  # 🔥 reseta fase corretamente

    st.success(f"Você escolheu {linguagem_nome} 🚀")
    st.switch_page("fase")  # 🔥 melhor prática
