import streamlit as st
import json, os

st.set_page_config(page_title="CodeQuest - Ranking", page_icon="🏆", layout="wide")

from backend.session import init_session
from backend.supabase_client import supabase

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['usuario']}")
    st.metric("⚡ XP", st.session_state["xp"])
    st.metric("🏆 Nível", st.session_state["nivel"])
    st.divider()
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")
    if st.button("📚 Jogar", use_container_width=True, type="primary"):
        st.switch_page("pages/linguagem.py")
    if st.button("🚪 Sair", use_container_width=True):
        from backend.crud import logout_usuario
        logout_usuario()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.switch_page("pages/login.py")

st.title("🏆 Ranking Global")
st.caption("Os maiores conquistadores do CodeQuest")

# Busca top 50 usuários ordenados por XP
res = supabase.table("users").select("nome, xp, nivel").order("xp", desc=True).limit(50).execute()
jogadores = res.data or []

if not jogadores:
    st.info("Nenhum jogador no ranking ainda. Seja o primeiro! 🚀")
    st.stop()

# Medalhas para o pódio
medalhas = {1: "🥇", 2: "🥈", 3: "🥉"}

# Destaque do pódio
if len(jogadores) >= 3:
    st.subheader("🎖️ Pódio")
    col1, col2, col3 = st.columns(3)

    with col2:
        st.markdown(f"### 🥇 1º lugar")
        st.metric(jogadores[0]["nome"], f"{jogadores[0]['xp']} XP")
        st.caption(f"Nível {jogadores[0]['nivel']}")

    with col1:
        st.markdown(f"### 🥈 2º lugar")
        st.metric(jogadores[1]["nome"], f"{jogadores[1]['xp']} XP")
        st.caption(f"Nível {jogadores[1]['nivel']}")

    with col3:
        st.markdown(f"### 🥉 3º lugar")
        st.metric(jogadores[2]["nome"], f"{jogadores[2]['xp']} XP")
        st.caption(f"Nível {jogadores[2]['nivel']}")

st.divider()

# Tabela completa
st.subheader("📋 Classificação Completa")

usuario_atual = st.session_state["usuario"]
sua_posicao = None

for i, jogador in enumerate(jogadores):
    posicao = i + 1
    eh_voce = jogador["nome"] == usuario_atual

    if eh_voce:
        sua_posicao = posicao

    medalha = medalhas.get(posicao, f"#{posicao}")

    if eh_voce:
        st.success(f"{medalha} &nbsp; **{jogador['nome']}** ← você &nbsp;|&nbsp; ⚡ {jogador['xp']} XP &nbsp;|&nbsp; 🏆 Nível {jogador['nivel']}")
    else:
        st.markdown(f"{medalha} &nbsp; {jogador['nome']} &nbsp;|&nbsp; ⚡ {jogador['xp']} XP &nbsp;|&nbsp; 🏆 Nível {jogador['nivel']}")

if sua_posicao:
    st.divider()
    st.info(f"🎯 Você está na **{sua_posicao}ª posição** do ranking!")
