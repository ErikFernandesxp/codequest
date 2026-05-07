import streamlit as st

st.set_page_config(page_title="CodeQuest - Fase", page_icon="🎯", layout="wide")

import json
import os
from backend.session import init_session, calcular_nivel
from backend.validator import validar_codigo
from backend.crud import salvar_progresso, atualizar_xp_nivel

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

# ─── Carregar fases ─────────────────────────────────────────────────────────
@st.cache_data
def carregar_fases():
    caminho = os.path.join(os.getcwd(), "data", "fases.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()

ling = st.session_state.get("linguagem")
fase_idx = st.session_state.get("fase", 0)

if not ling or ling not in fases:
    st.error("❌ Linguagem inválida. Volte e escolha uma linguagem.")
    if st.button("← Escolher linguagem"):
        st.switch_page("pages/linguagem.py")
    st.stop()

# ─── Sidebar HUD ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['usuario']}")
    st.metric("⚡ XP", st.session_state["xp"])
    st.metric("🏆 Nível", st.session_state["nivel"])
    xp_mod = st.session_state["xp"] % 50
    st.progress(xp_mod / 50, text=f"XP para próx. nível: {xp_mod}/50")
    st.metric("❤️ Vidas", st.session_state["vidas"])
    st.divider()
    lang_icons = {"python": "🐍", "c": "⚙️", "java": "☕", "php": "🌐"}
    total = len(fases[ling])
    st.progress(fase_idx / total if total else 0,
                text=f"{lang_icons.get(ling,'')} {ling.upper()}: fase {fase_idx+1}/{total}")
    st.divider()
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")

# ─── Game Over ────────────────────────────────────────────────────────────────
if st.session_state["vidas"] <= 0:
    st.error("💀 Game Over! Você ficou sem vidas.")
    if st.button("🔄 Recomeçar"):
        st.session_state.update({"vidas": 3, "fase": 0, "desafio_atual": 0})
        st.rerun()
    st.stop()

# ─── Fim do jogo ─────────────────────────────────────────────────────────────
if fase_idx >= len(fases[ling]):
    st.balloons()
    st.success("🎉 Parabéns! Você finalizou todas as fases desta linguagem!")
    st.metric("⚡ XP Total", st.session_state["xp"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Escolher outra linguagem", use_container_width=True, type="primary"):
            st.switch_page("pages/linguagem.py")
    with col2:
        if st.button("🔄 Reiniciar trilha", use_container_width=True):
            st.session_state.update({"fase": 0, "desafio_atual": 0, "vidas": 3})
            st.rerun()
    st.stop()

fase = fases[ling][fase_idx]

if not isinstance(fase, dict) or "desafios" not in fase:
    st.error("❌ Erro nos dados da fase.")
    st.stop()

desafios = fase["desafios"]
idx = st.session_state.get("desafio_atual", 0)

if idx >= len(desafios):
    st.session_state["desafio_atual"] = 0
    st.rerun()

desafio = desafios[idx]

# Compatibilidade com formato antigo (string)
if isinstance(desafio, str):
    respostas = fase.get("respostas", [])
    desafio = {
        "pergunta": desafio,
        "resposta": respostas[idx] if idx < len(respostas) else "",
        "dica": "Revise o exemplo acima",
        "erro_comum": "Erro de sintaxe",
        "explicacao": "Observe o exemplo da fase",
        "logica": "Siga o padrão apresentado"
    }

# ─── Interface ────────────────────────────────────────────────────────────────
st.title(f"🎯 Fase {fase_idx + 1} — {fase.get('titulo', '')}")
st.caption(f"Desafio {idx + 1} de {len(desafios)}")
st.progress((idx + 1) / len(desafios))

col1, col2 = st.columns([1, 1])

with col1:
    st.info(f"📖 **Conceito:** {fase.get('explicacao', '')}")
    st.warning(f"💡 **Dica:** {desafio.get('dica', 'Pense na lógica')}")

with col2:
    st.markdown("**📌 Exemplo:**")
    st.code(fase.get("exemplo", ""), language=ling if ling != "c" else "c")

st.divider()
st.markdown(f"### 🧩 {desafio.get('pergunta', '')}")

resposta = st.text_area("💻 Digite seu código:", height=120, key=f"input_{fase_idx}_{idx}",
                         placeholder="Escreva sua resposta aqui...")

col_btn1, col_btn2, _ = st.columns([1, 1, 3])
enviar = col_btn1.button("🚀 Enviar", type="primary", use_container_width=True)
pular = col_btn2.button("⏭️ Pular", use_container_width=True)

if pular:
    st.session_state["desafio_atual"] += 1
    if st.session_state["desafio_atual"] >= len(desafios):
        st.session_state["fase"] += 1
        st.session_state["desafio_atual"] = 0
    st.rerun()

if enviar:
    if not resposta.strip():
        st.warning("Digite algo antes de enviar!")
    else:
        ok, feedback = validar_codigo(resposta, desafio.get("resposta", ""))

        if ok:
            st.success("✅ Correto! Muito bem!")
            st.toast("🚀 +10 XP!")

            # Atualiza XP e nível
            novo_xp = st.session_state["xp"] + 10
            novo_nivel = calcular_nivel(novo_xp)
            subiu_nivel = novo_nivel > st.session_state["nivel"]

            st.session_state["xp"] = novo_xp
            st.session_state["nivel"] = novo_nivel

            # Persiste no Supabase
            atualizar_xp_nivel(st.session_state["user_id"], novo_xp, novo_nivel)

            st.session_state["desafio_atual"] += 1

            if st.session_state["desafio_atual"] >= len(desafios):
                st.success("🏆 Fase concluída! Indo para a próxima...")
                salvar_progresso(st.session_state["user_id"], ling, fase_idx)
                st.session_state["fase"] += 1
                st.session_state["desafio_atual"] = 0

            if subiu_nivel:
                st.balloons()
                st.success(f"🎉 Subiu para o Nível {novo_nivel}!")

            st.rerun()

        else:
            st.session_state["vidas"] -= 1
            vidas_rest = st.session_state["vidas"]

            st.error(f"❌ Resposta incorreta! ({vidas_rest} {'vida' if vidas_rest == 1 else 'vidas'} restante{'s' if vidas_rest != 1 else ''})")

            with st.expander("🧑‍🏫 Ver dica do professor", expanded=True):
                st.warning(f"💡 **Dica:** {desafio.get('dica', '')}")
                st.info(f"⚠️ **Erro comum:** {desafio.get('erro_comum', '')}")
                st.success(f"📘 **Explicação:** {desafio.get('explicacao', '')}")
                st.markdown(f"🧠 **Lógica:** {desafio.get('logica', '')}")
