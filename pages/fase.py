import streamlit as st
import json
import os
from backend.session import init_session
from backend.validator import validar_codigo

st.set_page_config(layout="wide")

init_session(st)

# 🔥 carregar JSON com segurança
@st.cache_data
def carregar_fases():
    caminho = os.path.join(os.getcwd(), "data", "fases.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()

ling = st.session_state.get("linguagem")
fase_idx = st.session_state.get("fase", 0)

# 🔐 valida linguagem
if not ling or ling not in fases:
    st.error("❌ Linguagem inválida")
    st.stop()

# 🔐 fim do jogo
if fase_idx >= len(fases[ling]):
    st.success("🎉 Você finalizou o jogo!")
    st.stop()

fase = fases[ling][fase_idx]

# 🔐 valida estrutura básica
if not isinstance(fase, dict):
    st.error("❌ Fase inválida no JSON")
    st.stop()

if "desafios" not in fase:
    st.error("❌ JSON sem desafios")
    st.stop()

desafios = fase["desafios"]
idx = st.session_state.get("desafio_atual", 0)

if idx >= len(desafios):
    st.session_state["desafio_atual"] = 0
    st.rerun()

desafio = desafios[idx]

# 🔥 COMPATIBILIDADE (JSON ANTIGO vs NOVO)
if isinstance(desafio, str):
    respostas = fase.get("respostas", [])
    resposta_correta = respostas[idx] if idx < len(respostas) else ""

    desafio = {
        "pergunta": desafio,
        "resposta": resposta_correta,
        "dica": "Revise o exemplo acima",
        "erro_comum": "Erro de sintaxe",
        "explicacao": "Observe como o código funciona no exemplo",
        "logica": "Siga o padrão apresentado"
    }

# 🔐 valida final
if not isinstance(desafio, dict):
    st.error("❌ Erro no formato do desafio")
    st.stop()

# 🎮 HUD
st.sidebar.metric("XP", st.session_state["xp"])
st.sidebar.metric("Nível", st.session_state["nivel"])
st.sidebar.metric("❤️ Vidas", st.session_state["vidas"])

# 💀 GAME OVER
if st.session_state["vidas"] <= 0:
    st.error("💀 Game Over")

    if st.button("🔄 Recomeçar"):
        st.session_state["vidas"] = 3
        st.session_state["fase"] = 0
        st.session_state["desafio_atual"] = 0
        st.rerun()

    st.stop()

# 🎯 INTERFACE
st.title(f"🎯 Fase {fase_idx + 1} - {fase.get('titulo','')}")

col1, col2 = st.columns(2)

with col1:
    st.info(fase.get("explicacao", ""))
    st.warning("💡 " + desafio.get("dica", "Pense na lógica"))

with col2:
    st.code(fase.get("exemplo", ""), language=ling)

# 📊 progresso
st.progress((idx + 1) / len(desafios))

# 🧩 desafio
st.markdown(f"### 🧩 Desafio {idx + 1}")
st.write(desafio.get("pergunta", ""))

resposta = st.text_area("💻 Digite seu código", key=f"input_{idx}")

# 🚀 envio
if st.button("Enviar"):

    ok, feedback = validar_codigo(resposta, desafio.get("resposta", ""))

    if ok:
        st.success("✅ Correto!")

        st.session_state["xp"] += 10
        st.session_state["desafio_atual"] += 1

        # passou da fase
        if st.session_state["desafio_atual"] >= len(desafios):
            st.success("🏆 Fase concluída!")

            st.session_state["fase"] += 1
            st.session_state["desafio_atual"] = 0

        st.rerun()

    else:
        st.session_state["vidas"] -= 1

        st.error("❌ Errou")

        st.markdown("## 🧑‍🏫 Professor")

        st.warning(f"💡 Dica: {desafio.get('dica','')}")

        st.info(f"⚠️ Erro comum: {desafio.get('erro_comum','')}")

        st.success(f"📘 Explicação: {desafio.get('explicacao','')}")

        st.markdown(f"🧠 **Lógica:** {desafio.get('logica','')}")
