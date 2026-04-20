import streamlit as st
import json
from backend.validator import validar_codigo

with open("data/fases.json") as f:
    fases = json.load(f)

linguagem = st.session_state.get("linguagem", "python").lower()

fase_atual = 0

fase = fases[linguagem][fase_atual]

st.title(f"Fase {fase['fase']} - {fase['titulo']}")
st.write(fase["explicacao"])

resposta = st.text_area("Digite seu código")

if st.button("Enviar"):
    correto, feedback = validar_codigo(resposta, fase["resposta"])
    
    if correto:
        st.success(feedback)
    else:
        st.error(feedback)