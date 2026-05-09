import streamlit as st

st.set_page_config(page_title="CodeQuest", page_icon="🎮", layout="wide",
                   initial_sidebar_state="collapsed")

import json, os
from backend.session import init_session, verificar_admin
from backend.crud import (buscar_progresso, logout_usuario, atualizar_streak,
                           calcular_vidas_regeneradas, atualizar_vidas,
                           buscar_perfil, verificar_e_conceder_badges)
from backend.theme import CSS

init_session(st)

# ── Restaura sessão dos query_params ─────────────────────────────────────────
if not st.session_state.get("logado"):
    params = st.query_params
    if "uid" in params:
        try:
            uid      = params["uid"]
            email    = params.get("em", "")
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
    display:flex; align-items:center; justify-content:space-between;
    padding:14px 28px; background:#1c1f27;
    border-bottom:1.5px solid #2e3240;
    margin-bottom:28px; border-radius:0 0 14px 14px;
    flex-wrap:wrap; gap:8px;
}
.nav-logo { font-size:1.35rem; font-weight:800; color:#f4f3ee; }
.nav-logo span { color:#7c6af7; }
.nav-right { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
.nav-chip {
    background:#252833; border:1px solid #2e3240;
    padding:5px 14px; border-radius:20px;
    font-size:0.8rem; color:#b0b3c1; font-weight:600;
}
.admin-chip {
    background:#2a1f5e; border:1px solid #4c3fa0;
    padding:4px 12px; border-radius:20px;
    font-size:0.72rem; color:#a78bfa; font-weight:700;
    text-transform:uppercase; letter-spacing:0.5px;
}
.nav-avatar {
    width:34px; height:34px; border-radius:50%;
    background:linear-gradient(135deg,#7c6af7,#a78bfa);
    display:flex; align-items:center; justify-content:center;
    font-weight:800; font-size:0.85rem; color:#fff;
}
.sec-title {
    font-size:0.72rem; color:#7a7d8e; font-weight:700;
    text-transform:uppercase; letter-spacing:1.5px;
    margin:28px 0 12px;
}
.lang-card {
    background:#1c1f27; border:1.5px solid #2e3240;
    border-radius:16px; padding:22px 18px;
    transition:border-color 0.2s, transform 0.2s;
    height:100%;
}
.lang-icon { font-size:2.4rem; margin-bottom:10px; }
.lang-name { font-size:1rem; font-weight:700; color:#f4f3ee; }
.lang-prog { font-size:0.78rem; color:#b0b3c1; margin:4px 0 10px; }
.lang-bar-bg { background:#252833; border-radius:4px; height:5px; }
.lang-bar-fill {
    background:linear-gradient(90deg,#7c6af7,#a78bfa);
    height:5px; border-radius:4px;
}
.badge-chip {
    display:inline-flex; align-items:center; gap:6px;
    background:#1c1f27; border:1.5px solid #2e3240;
    border-radius:20px; padding:6px 14px; margin:4px;
    font-size:0.82rem; color:#f4f3ee; font-weight:500;
}
.empty-state { color:#7a7d8e; font-size:0.88rem; }
.xp-bg { background:#252833; border-radius:6px; height:8px; margin-top:6px; }
.xp-fill { background:linear-gradient(90deg,#7c6af7,#a78bfa); height:8px; border-radius:6px; }
.stat-box {
    background:#111318; border:1.5px solid #2e3240;
    border-radius:14px; padding:14px 10px; text-align:center;
}
.stat-val { font-size:1.4rem; font-weight:800; color:#f4f3ee; }
.stat-lbl { font-size:0.65rem; color:#7a7d8e; text-transform:uppercase;
            letter-spacing:0.5px; margin-top:2px; }
@media (max-width: 768px) {
    .navbar { padding:10px 16px; }
    .stat-val { font-size:1rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Carrega dados ─────────────────────────────────────────────────────────────
user_id  = st.session_state["user_id"]
is_admin = st.session_state.get("is_admin", False)
perfil   = buscar_perfil(user_id)

if perfil:
    st.session_state["streak"]  = atualizar_streak(user_id, perfil)
    st.session_state["xp"]      = perfil.get("xp", 0)
    st.session_state["nivel"]   = perfil.get("nivel", 1)
    st.session_state["usuario"] = perfil.get("nome", st.session_state["usuario"])
    if not is_admin:
        vn = calcular_vidas_regeneradas(perfil.get("ultima_vida",""), perfil.get("vidas",3))
        if vn != perfil.get("vidas",3):
            atualizar_vidas(user_id, vn)
        st.session_state["vidas"] = vn

usuario  = st.session_state["usuario"]
xp       = st.session_state["xp"]
nivel    = st.session_state["nivel"]
streak   = st.session_state.get("streak", 0)
vidas    = st.session_state.get("vidas", 3)
xp_mod   = xp % 50
xp_pct   = int(xp_mod / 50 * 100)
inicial  = usuario[0].upper() if usuario else "?"
vidas_str = "inf" if is_admin else str(vidas)

@st.cache_data
def fases_json():
    with open(os.path.join(os.getcwd(),"data","fases.json"), encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def badges_json():
    with open(os.path.join(os.getcwd(),"data","badges.json"), encoding="utf-8") as f:
        return json.load(f)

fases         = fases_json()
badges_config = badges_json()
progresso     = buscar_progresso(user_id)
concluidas    = {}
for p in progresso:
    if p.get("concluido", False):
        concluidas[p["linguagem"]] = concluidas.get(p["linguagem"], 0) + 1

total_c = sum(concluidas.values())
novas, _ = verificar_e_conceder_badges(user_id, perfil or {}, total_c, fases_por_lang=concluidas)
for b in novas:
    cfg = badges_config.get(b, {})
    st.toast("🏅 " + cfg.get("emoji","") + " " + cfg.get("nome",""), icon="🎉")

# ── Navbar ────────────────────────────────────────────────────────────────────
admin_html = '<div class="admin-chip">Admin</div>' if is_admin else ""
st.markdown(
    '<div class="navbar">'
    '<div class="nav-logo">Code<span>Quest</span></div>'
    '<div class="nav-right">'
    + admin_html
    + '<div class="nav-chip">' + str(xp) + ' XP</div>'
    + '<div class="nav-chip">Nv.' + str(nivel) + '</div>'
    + '<div class="nav-avatar">' + inicial + '</div>'
    + '<span style="color:#f4f3ee;font-weight:600;font-size:0.92rem;">' + usuario + '</span>'
    + '</div></div>',
    unsafe_allow_html=True
)

# ── Hero ──────────────────────────────────────────────────────────────────────
modo = "Modo Admin" if is_admin else "Bem-vindo de volta"

col_l, col_r = st.columns([2, 1])
with col_l:
    st.markdown(
        '<div style="background:#1c1f27;border:1.5px solid #2e3240;border-radius:18px;padding:28px 32px;margin-bottom:24px;">'
        '<div style="font-size:0.72rem;color:#7c6af7;font-weight:700;text-transform:uppercase;letter-spacing:1px;">' + modo + '</div>'
        '<div style="font-size:1.9rem;font-weight:800;color:#f4f3ee;margin-top:4px;">' + usuario + ' 👋</div>'
        + ('<div style="font-size:0.85rem;color:#fbbf24;margin-top:4px;">🔥 ' + str(streak) + ' dias seguidos</div>' if streak >= 2 else '')
        + '<div style="font-size:0.75rem;color:#b0b3c1;margin-top:14px;">Nivel ' + str(nivel) + ' &rarr; ' + str(nivel+1) + ' &nbsp; ' + str(xp_mod) + ' / 50 XP</div>'
        + '<div class="xp-bg"><div class="xp-fill" style="width:' + str(xp_pct) + '%"></div></div>'
        + '</div>',
        unsafe_allow_html=True
    )

with col_r:
    st.markdown('<div style="background:#1c1f27;border:1.5px solid #2e3240;border-radius:18px;padding:28px 16px;margin-bottom:24px;">', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="stat-box"><div class="stat-val">' + str(xp) + '</div><div class="stat-lbl">XP</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-box"><div class="stat-val">' + str(nivel) + '</div><div class="stat-lbl">Nivel</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-box"><div class="stat-val">' + vidas_str + '</div><div class="stat-lbl">Vidas</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="stat-box"><div class="stat-val">' + str(streak) + '</div><div class="stat-lbl">Dias</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Botoes ────────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    if st.button("🚀  Jogar — Escolher Linguagem", use_container_width=True, type="primary"):
        st.switch_page("pages/linguagem.py")
with c2:
    if st.button("🏆  Ranking", use_container_width=True):
        st.switch_page("pages/ranking.py")
with c3:
    if st.button("🚪  Sair", use_container_width=True):
        logout_usuario()
        st.query_params.clear()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.switch_page("pages/login.py")

# ── Trilhas ───────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-title">📊 Suas Trilhas</div>', unsafe_allow_html=True)
lang_data = [("python","🐍","Python"), ("c","⚙️","C"),
             ("java","☕","Java"),    ("php","🌐","PHP")]
cols = st.columns(4)
for i, (lang, icon, label) in enumerate(lang_data):
    total  = len(fases.get(lang, []))
    feitas = concluidas.get(lang, 0)
    pct    = int(feitas / total * 100) if total else 0
    with cols[i]:
        st.markdown(
            '<div class="lang-card">'
            '<div class="lang-icon">' + icon + '</div>'
            '<div class="lang-name">' + label + '</div>'
            '<div class="lang-prog">' + str(feitas) + "/" + str(total) + " fases &nbsp; " + str(pct) + "%</div>"
            '<div class="lang-bar-bg"><div class="lang-bar-fill" style="width:' + str(pct) + '%"></div></div>'
            '</div>',
            unsafe_allow_html=True
        )

# ── Conquistas ────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-title">🏅 Conquistas</div>', unsafe_allow_html=True)
badges_user = perfil.get("badges", []) if perfil else []
if badges_user:
    html = "".join(
        '<div class="badge-chip">'
        + badges_config.get(b, {}).get("emoji", "🏅") + " "
        + badges_config.get(b, {}).get("nome", b)
        + '</div>'
        for b in badges_user
    )
    st.markdown('<div style="display:flex;flex-wrap:wrap;gap:4px;">' + html + '</div>',
                unsafe_allow_html=True)
else:
    st.markdown('<p class="empty-state">Nenhuma conquista ainda. Jogue para ganhar badges! 🎯</p>',
                unsafe_allow_html=True)
