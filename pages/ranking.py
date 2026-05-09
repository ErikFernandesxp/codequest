import streamlit as st

st.set_page_config(page_title="CodeQuest — Ranking", page_icon="🏆", layout="wide",
                   initial_sidebar_state="collapsed")

from backend.session import init_session, verificar_admin
from backend.crud import buscar_perfil
from backend.supabase_client import supabase
from backend.theme import CSS

init_session(st)

# ── Restaura sessão dos query_params se necessário ────────────────────────────
if not st.session_state.get("logado"):
    params = st.query_params
    if "uid" in params:
        try:
            uid   = params["uid"]
            email = params.get("em", "")
            perfil_r = buscar_perfil(uid)
            if perfil_r:
                is_admin_r = verificar_admin(email)
                st.session_state.update({
                    "logado":        True,
                    "user_id":       uid,
                    "usuario_email": email,
                    "is_admin":      is_admin_r,
                    "usuario":       perfil_r.get("nome", email.split("@")[0]),
                    "xp":            perfil_r.get("xp", 0),
                    "nivel":         perfil_r.get("nivel", 1),
                    "vidas":         999 if is_admin_r else perfil_r.get("vidas", 3),
                })
        except Exception:
            pass

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

st.markdown(CSS, unsafe_allow_html=True)
st.markdown("""
<style>
.navbar {
    display:flex; align-items:center; padding:14px 28px;
    background:#1c1f27; border-bottom:1.5px solid #2e3240;
    margin-bottom:28px; border-radius:0 0 14px 14px;
}
.nav-logo { font-size:1.35rem; font-weight:800; color:#f4f3ee; }
.nav-logo span { color:#7c6af7; }

.podium { background:#1c1f27; border:2px solid #2e3240;
          border-radius:18px; padding:28px 16px; text-align:center; }
.pod-1  { border-color:#f59e0b; background:linear-gradient(160deg,#1a1710,#1c1f27); }
.pod-2  { border-color:#6b7280; }
.pod-3  { border-color:#92400e; }
.pod-medal { font-size:2.8rem; }
.pod-name  { font-size:1rem; font-weight:700; color:#f4f3ee; margin:6px 0 2px; }
.pod-xp    { font-size:1.4rem; font-weight:800; color:#7c6af7; }
.pod-nivel { font-size:0.75rem; color:#b0b3c1; margin-top:2px; }

.rank-row {
    display:flex; align-items:center;
    background:#1c1f27; border:1.5px solid #2e3240;
    border-radius:12px; padding:13px 20px; margin-bottom:7px;
}
.rank-row.you { border-color:#7c6af7; background:#1a1830; }
.rank-pos  { font-family:'DM Mono',monospace; font-size:0.88rem;
             color:#b0b3c1; font-weight:700; min-width:44px; }
.rank-name { flex:1; font-weight:600; color:#f4f3ee; font-size:0.95rem; }
.rank-xp   { font-family:'DM Mono',monospace; font-size:0.9rem;
             font-weight:700; color:#7c6af7; }
.rank-nv   { font-size:0.75rem; color:#7a7d8e; margin-left:14px; }
.you-tag {
    display:inline-block; background:#7c6af7; color:#fff;
    padding:2px 8px; border-radius:20px;
    font-size:0.68rem; font-weight:700; margin-left:8px;
}

@media (max-width: 768px) {
    .navbar { padding:10px 16px; }
    .rank-row { padding:10px 14px; }
    .rank-nv { display:none; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="navbar"><div class="nav-logo">Code<span>Quest</span></div></div>',
            unsafe_allow_html=True)

if st.button("← Voltar ao Menu"):
    st.switch_page("pages/dashboard.py")

st.markdown("<h2 style='font-size:1.7rem;font-weight:800;margin:16px 0 4px;color:#f4f3ee;'>🏆 Ranking Global</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#b0b3c1;margin-bottom:24px;font-size:0.88rem;'>Os maiores conquistadores do CodeQuest</p>", unsafe_allow_html=True)

res       = supabase.table("users").select("nome,xp,nivel").order("xp", desc=True).limit(50).execute()
jogadores = res.data or []
usuario   = st.session_state["usuario"]
medalhas  = {1:"🥇", 2:"🥈", 3:"🥉"}

if not jogadores:
    st.info("Nenhum jogador ainda. Seja o primeiro! 🚀")
    st.stop()

# ── Pódio top 3 ───────────────────────────────────────────────────────────────
if len(jogadores) >= 3:
    c2, c1, c3 = st.columns(3)
    def pod_card(j, cls, medal):
        return f'<div class="podium {cls}"><div class="pod-medal">{medal}</div><div class="pod-name">{j["nome"]}</div><div class="pod-xp">{j["xp"]} XP</div><div class="pod-nivel">Nível {j["nivel"]}</div></div>'
    with c1: st.markdown(pod_card(jogadores[0], "pod-1", "🥇"), unsafe_allow_html=True)
    with c2: st.markdown(pod_card(jogadores[1], "pod-2", "🥈"), unsafe_allow_html=True)
    with c3: st.markdown(pod_card(jogadores[2], "pod-3", "🥉"), unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

st.markdown("<div style='font-size:0.72rem;color:#7a7d8e;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px;'>Classificação completa</div>", unsafe_allow_html=True)

# ── Lista completa ────────────────────────────────────────────────────────────
sua_pos = None
for i, j in enumerate(jogadores):
    pos   = i + 1
    eh_vc = j["nome"] == usuario
    if eh_vc:
        sua_pos = pos
    medal  = medalhas.get(pos, f"#{pos:02d}")
    classe = "rank-row you" if eh_vc else "rank-row"
    tag    = '<span class="you-tag">você</span>' if eh_vc else ""
    st.markdown(f"""
    <div class="{classe}">
      <div class="rank-pos">{medal}</div>
      <div class="rank-name">{j["nome"]}{tag}</div>
      <div class="rank-nv">Nv.{j["nivel"]}</div>
      <div class="rank-xp">{j["xp"]} XP</div>
    </div>
    """, unsafe_allow_html=True)

if sua_pos:
    st.markdown(f"<div style='text-align:center;margin-top:20px;color:#7c6af7;font-weight:700;font-size:0.9rem;'>🎯 Você está na {sua_pos}ª posição!</div>", unsafe_allow_html=True)
