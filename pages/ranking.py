import streamlit as st

st.set_page_config(page_title="CodeQuest — Ranking", page_icon="🏆", layout="wide", initial_sidebar_state="collapsed")

from backend.session import init_session
from backend.supabase_client import supabase

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0f0f13; color: #f0efe8; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 28px; background: #16161d;
    border-bottom: 1px solid #2a2a35; margin-bottom: 32px;
    border-radius: 0 0 16px 16px;
}
.nav-logo { font-size: 1.4rem; font-weight: 800; }
.nav-logo span { color: #7c6af7; }

.podium-card {
    background: #16161d; border: 1px solid #2a2a35;
    border-radius: 20px; padding: 28px 20px; text-align: center;
}
.podium-1 { border-color: #f59e0b; background: linear-gradient(135deg,#1a1710,#16161d); }
.podium-2 { border-color: #6b7280; }
.podium-3 { border-color: #92400e; }
.podium-medal { font-size: 2.5rem; margin-bottom: 8px; }
.podium-name { font-size: 1rem; font-weight: 700; color: #f0efe8; }
.podium-xp { font-size: 1.4rem; font-weight: 800; color: #7c6af7; margin: 4px 0; }
.podium-nivel { font-size: 0.78rem; color: #9b9ba8; }

.rank-row {
    display: flex; align-items: center;
    background: #16161d; border: 1px solid #2a2a35;
    border-radius: 12px; padding: 14px 20px; margin-bottom: 8px;
    transition: border-color 0.2s;
}
.rank-row:hover { border-color: #3a3a4a; }
.rank-row.you { border-color: #7c6af7; background: #1a1830; }
.rank-pos { font-size: 0.9rem; font-weight: 700; color: #9b9ba8;
    min-width: 40px; font-family: 'DM Mono', monospace; }
.rank-name { flex: 1; font-weight: 600; color: #f0efe8; }
.rank-xp { font-size: 0.9rem; font-weight: 700; color: #7c6af7;
    font-family: 'DM Mono', monospace; }
.rank-nivel { font-size: 0.78rem; color: #9b9ba8; margin-left: 16px; }

.stButton button {
    border-radius: 12px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <div class="nav-logo">Code<span>Quest</span></div>
</div>
""", unsafe_allow_html=True)

if st.button("← Voltar ao Menu"):
    st.switch_page("pages/dashboard.py")

st.markdown("<h2 style='font-size:1.8rem;font-weight:800;margin:20px 0 4px;'>🏆 Ranking Global</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#9b9ba8;margin-bottom:28px;'>Os maiores conquistadores do CodeQuest</p>", unsafe_allow_html=True)

res = supabase.table("users").select("nome, xp, nivel").order("xp", desc=True).limit(50).execute()
jogadores = res.data or []

if not jogadores:
    st.info("Nenhum jogador ainda. Seja o primeiro! 🚀")
    st.stop()

usuario_atual = st.session_state["usuario"]
medalhas = {1:"🥇", 2:"🥈", 3:"🥉"}

# Pódio
if len(jogadores) >= 3:
    st.markdown("<div style='margin-bottom:24px;'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c2:
        p = jogadores[0]
        st.markdown(f'<div class="podium-card podium-1"><div class="podium-medal">🥇</div><div class="podium-name">{p["nome"]}</div><div class="podium-xp">{p["xp"]} XP</div><div class="podium-nivel">Nível {p["nivel"]}</div></div>', unsafe_allow_html=True)
    with c1:
        p = jogadores[1]
        st.markdown(f'<div class="podium-card podium-2"><div class="podium-medal">🥈</div><div class="podium-name">{p["nome"]}</div><div class="podium-xp">{p["xp"]} XP</div><div class="podium-nivel">Nível {p["nivel"]}</div></div>', unsafe_allow_html=True)
    with c3:
        p = jogadores[2]
        st.markdown(f'<div class="podium-card podium-3"><div class="podium-medal">🥉</div><div class="podium-name">{p["nome"]}</div><div class="podium-xp">{p["xp"]} XP</div><div class="podium-nivel">Nível {p["nivel"]}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='font-size:0.75rem;color:#9b9ba8;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin:24px 0 12px;'>Classificação Completa</div>", unsafe_allow_html=True)

sua_posicao = None
for i, j in enumerate(jogadores):
    pos = i + 1
    eh_voce = j["nome"] == usuario_atual
    if eh_voce:
        sua_posicao = pos
    medalha = medalhas.get(pos, f"#{pos:02d}")
    classe = "rank-row you" if eh_voce else "rank-row"
    voce_label = " <span style='font-size:0.7rem;background:#7c6af7;color:white;padding:2px 8px;border-radius:20px;margin-left:8px;'>você</span>" if eh_voce else ""
    st.markdown(f"""
    <div class="{classe}">
        <div class="rank-pos">{medalha}</div>
        <div class="rank-name">{j["nome"]}{voce_label}</div>
        <div class="rank-nivel">Nv.{j["nivel"]}</div>
        <div class="rank-xp">{j["xp"]} XP</div>
    </div>
    """, unsafe_allow_html=True)

if sua_posicao:
    st.markdown(f"<div style='text-align:center;margin-top:20px;color:#7c6af7;font-weight:700;'>🎯 Você está na {sua_posicao}ª posição!</div>", unsafe_allow_html=True)
