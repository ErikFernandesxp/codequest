import streamlit as st

st.set_page_config(
    page_title="CodeQuest",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import json, os
from backend.session import init_session, calcular_nivel
from backend.gemini_validator import validar_resposta
from backend.crud import (
    salvar_progresso, atualizar_xp_nivel,
    calcular_vidas_regeneradas, atualizar_vidas,
    buscar_perfil, verificar_e_conceder_badges,
    buscar_progresso
)

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

is_admin = st.session_state.get("is_admin", False)

# CSS customizado
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0f0f13; color: #f0efe8; }

.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 24px; background: #16161d;
    border-bottom: 1px solid #2a2a35; margin-bottom: 24px;
    border-radius: 0 0 12px 12px;
}
.topbar-left { display: flex; align-items: center; gap: 16px; }
.topbar-logo { font-size: 1.3rem; font-weight: 800; color: #f0efe8; letter-spacing: -0.5px; }
.topbar-lang {
    background: #2a2a35; padding: 4px 12px; border-radius: 20px;
    font-size: 0.8rem; color: #9b9ba8; font-family: 'DM Mono', monospace;
}
.topbar-right { display: flex; align-items: center; gap: 20px; }
.stat-pill {
    display: flex; align-items: center; gap: 6px;
    background: #1e1e28; padding: 6px 14px; border-radius: 20px;
    font-size: 0.85rem; font-weight: 600;
}

.fase-header {
    background: linear-gradient(135deg, #1a1a24 0%, #16161d 100%);
    border: 1px solid #2a2a35; border-radius: 16px;
    padding: 20px 28px; margin-bottom: 20px;
}
.fase-titulo { font-size: 1.4rem; font-weight: 800; color: #f0efe8; margin: 0 0 8px 0; }
.fase-progress-bar {
    background: #2a2a35; border-radius: 4px; height: 6px; margin-top: 12px;
}
.fase-progress-fill {
    background: linear-gradient(90deg, #7c6af7, #a78bfa);
    height: 6px; border-radius: 4px; transition: width 0.4s ease;
}

.conceito-box {
    background: #1a1a24; border: 1px solid #2a2a35;
    border-left: 3px solid #7c6af7;
    border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;
}
.dica-box {
    background: #1a2218; border: 1px solid #2a3528;
    border-left: 3px solid #4ade80;
    border-radius: 12px; padding: 16px 20px;
}

.pergunta-box {
    background: #16161d; border: 2px solid #2a2a35;
    border-radius: 16px; padding: 24px 28px; margin: 20px 0;
}
.pergunta-label { font-size: 0.75rem; color: #7c6af7; text-transform: uppercase;
    letter-spacing: 1px; font-weight: 700; margin-bottom: 10px; }
.pergunta-texto { font-size: 1.1rem; font-weight: 600; color: #f0efe8; line-height: 1.5; }

.btn-enviar {
    background: linear-gradient(135deg, #7c6af7, #a78bfa) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
}
.btn-pular {
    background: #1e1e28 !important; color: #9b9ba8 !important;
    border: 1px solid #2a2a35 !important; border-radius: 10px !important;
}

.feedback-ok {
    background: #0d2416; border: 1px solid #166534;
    border-radius: 12px; padding: 16px 20px; margin-top: 16px;
}
.feedback-erro {
    background: #1f0a0a; border: 1px solid #7f1d1d;
    border-radius: 12px; padding: 16px 20px; margin-top: 16px;
}
.professor-box {
    background: #1a1824; border: 1px solid #312e5a;
    border-radius: 12px; padding: 20px; margin-top: 12px;
}
.gemini-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #1a2035; border: 1px solid #2a3a6a;
    border-radius: 20px; padding: 4px 12px;
    font-size: 0.72rem; color: #60a5fa; font-weight: 600;
    margin-bottom: 12px;
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
div[data-testid="stTextArea"] textarea {
    background: #1e1e28 !important; color: #f0efe8 !important;
    border: 1px solid #2a2a35 !important; border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.9rem !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #7c6af7 !important; box-shadow: 0 0 0 2px rgba(124,106,247,0.2) !important;
}
.stButton button {
    border-radius: 10px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important; transition: all 0.2s !important;
}
.stExpander { background: #1a1824 !important; border: 1px solid #2a2a35 !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("vidas_sincronizadas") and not is_admin:
    perfil = buscar_perfil(st.session_state["user_id"])
    if perfil:
        vidas_novas = calcular_vidas_regeneradas(
            perfil.get("ultima_vida", ""),
            perfil.get("vidas", 3)
        )
        st.session_state["vidas"] = vidas_novas
        st.session_state["vidas_sincronizadas"] = True

@st.cache_data
def carregar_fases():
    caminho = os.path.join(os.getcwd(), "data", "fases.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def carregar_badges_config():
    caminho = os.path.join(os.getcwd(), "data", "badges.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()
badges_config = carregar_badges_config()

ling = st.session_state.get("linguagem")
fase_idx = st.session_state.get("fase", 0)
lang_icons = {"python": "🐍", "c": "⚙️", "java": "☕", "php": "🌐"}

if not ling or ling not in fases:
    st.error("Linguagem inválida.")
    if st.button("← Escolher linguagem"):
        st.switch_page("pages/linguagem.py")
    st.stop()

vidas_display = "∞" if is_admin else st.session_state["vidas"]
xp = st.session_state["xp"]
nivel = st.session_state["nivel"]
streak = st.session_state.get("streak", 0)
total_fases = len(fases[ling])

# ─── Topbar ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div class="topbar-left">
        <span class="topbar-logo">🎮 CodeQuest</span>
        <span class="topbar-lang">{lang_icons.get(ling,'')} {ling.upper()} — Fase {fase_idx+1}/{total_fases}</span>
    </div>
    <div class="topbar-right">
        <div class="stat-pill">❤️ {vidas_display}</div>
        <div class="stat-pill">⚡ {xp} XP</div>
        <div class="stat-pill">🏆 Nv.{nivel}</div>
        <div class="stat-pill">🔥 {streak}d</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 8])
with col_nav1:
    if st.button("🏠 Menu"):
        st.session_state["vidas_sincronizadas"] = False
        st.switch_page("pages/dashboard.py")
with col_nav2:
    if st.button("📚 Trilhas"):
        st.switch_page("pages/linguagem.py")

# ─── Game Over ────────────────────────────────────────────────────────────────
if not is_admin and st.session_state["vidas"] <= 0:
    st.markdown("""
    <div style="text-align:center;padding:60px 0;">
        <div style="font-size:4rem;">💀</div>
        <h2 style="color:#f0efe8;">Game Over</h2>
        <p style="color:#9b9ba8;">Suas vidas regeneram 1 a cada 30 minutos.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🏠 Voltar ao Menu", use_container_width=True):
        st.session_state["vidas_sincronizadas"] = False
        st.switch_page("pages/dashboard.py")
    st.stop()

# ─── Fim da trilha ───────────────────────────────────────────────────────────
if fase_idx >= len(fases[ling]):
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center;padding:60px 0;">
        <div style="font-size:4rem;">🏆</div>
        <h2 style="color:#f0efe8;">Trilha concluída!</h2>
        <p style="color:#9b9ba8;">Você finalizou todas as fases de {ling.upper()}!</p>
        <p style="color:#7c6af7;font-size:1.2rem;font-weight:700;">⚡ {xp} XP acumulados</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 Outra linguagem", use_container_width=True, type="primary"):
            st.session_state["vidas_sincronizadas"] = False
            st.switch_page("pages/linguagem.py")
    with c2:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.update({"fase": 0, "desafio_atual": 0})
            st.rerun()
    st.stop()

fase = fases[ling][fase_idx]
if not isinstance(fase, dict) or "desafios" not in fase:
    st.error("Erro nos dados da fase.")
    st.stop()

desafios = fase["desafios"]
idx = st.session_state.get("desafio_atual", 0)
if idx >= len(desafios):
    st.session_state["desafio_atual"] = 0
    st.rerun()

desafio = desafios[idx]
if isinstance(desafio, str):
    desafio = {"pergunta": desafio, "resposta": "", "dica": "", "erro_comum": "", "explicacao": "", "logica": ""}

progresso_pct = int(((fase_idx * len(desafios) + idx) / (total_fases * len(desafios))) * 100)

# ─── Header da Fase ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="fase-header">
    <div class="fase-titulo">🎯 {fase.get('titulo','')}</div>
    <div style="color:#9b9ba8;font-size:0.85rem;">Desafio {idx+1} de {len(desafios)}</div>
    <div class="fase-progress-bar">
        <div class="fase-progress-fill" style="width:{int(((idx+1)/len(desafios))*100)}%"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Conteúdo ────────────────────────────────────────────────────────────────
col_esq, col_dir = st.columns([1, 1])

with col_esq:
    st.markdown(f"""
    <div class="conceito-box">
        <div style="font-size:0.72rem;color:#7c6af7;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:8px;">📖 Conceito</div>
        <div style="color:#d4d3cc;line-height:1.6;font-size:0.9rem;">{fase.get('explicacao','')}</div>
    </div>
    <div class="dica-box">
        <div style="font-size:0.72rem;color:#4ade80;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:8px;">💡 Dica</div>
        <div style="color:#d4d3cc;font-size:0.9rem;">{desafio.get('dica','')}</div>
    </div>
    """, unsafe_allow_html=True)

with col_dir:
    st.markdown("<div style='font-size:0.72rem;color:#9b9ba8;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:8px;'>📌 Exemplo</div>", unsafe_allow_html=True)
    st.code(fase.get("exemplo", ""), language=ling)

# ─── Pergunta ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="pergunta-box">
    <div class="pergunta-label">🧩 Desafio {idx+1}</div>
    <div class="pergunta-texto">{desafio.get('pergunta','')}</div>
</div>
""", unsafe_allow_html=True)

resposta = st.text_area(
    "💻 Seu código:",
    height=130,
    key=f"input_{fase_idx}_{idx}",
    placeholder="Digite sua resposta aqui..."
)

col_b1, col_b2, col_b3, _ = st.columns([1, 1, 1, 3])
enviar = col_b1.button("🚀 Enviar", type="primary", use_container_width=True)
pular  = col_b2.button("⏭️ Pular" + ("" if is_admin else " -1❤️"), use_container_width=True)
voltar = col_b3.button("🏠 Menu", use_container_width=True)

if voltar:
    st.session_state["vidas_sincronizadas"] = False
    st.switch_page("pages/dashboard.py")

if pular:
    if not is_admin:
        st.session_state["vidas"] -= 1
        atualizar_vidas(st.session_state["user_id"], st.session_state["vidas"])
    st.session_state["desafio_atual"] += 1
    if st.session_state["desafio_atual"] >= len(desafios):
        st.session_state["fase"] += 1
        st.session_state["desafio_atual"] = 0
    st.rerun()

if enviar:
    if not resposta.strip():
        st.warning("Digite algo antes de enviar!")
    else:
        with st.spinner("Verificando..."):
            correto, feedback, fonte = validar_resposta(
                pergunta=desafio.get("pergunta", ""),
                resposta_aluno=resposta,
                linguagem=ling,
                gabarito=desafio.get("resposta", ""),
                respostas_aceitas=desafio.get("respostas_aceitas", []),
                keywords=desafio.get("keywords", [])
            )

        if correto:
            gemini_badge = '<div class="gemini-badge">✨ Avaliado por IA</div>' if fonte == "gemini" else ""
            st.markdown(f"""
            <div class="feedback-ok">
                {gemini_badge}
                <div style="color:#4ade80;font-weight:700;font-size:1rem;">✅ Correto! Muito bem!</div>
                <div style="color:#86efac;margin-top:6px;font-size:0.9rem;">{feedback if feedback and feedback not in ['Correto!',''] else 'Solução perfeita!'}</div>
            </div>
            """, unsafe_allow_html=True)

            novo_xp = xp + 10
            novo_nivel = calcular_nivel(novo_xp)
            subiu = novo_nivel > nivel
            st.session_state.update({"xp": novo_xp, "nivel": novo_nivel})
            atualizar_xp_nivel(st.session_state["user_id"], novo_xp, novo_nivel)
            st.toast("🚀 +10 XP!")

            st.session_state["desafio_atual"] += 1
            if st.session_state["desafio_atual"] >= len(desafios):
                st.success("🏆 Fase concluída!")
                salvar_progresso(st.session_state["user_id"], ling, fase_idx)
                st.session_state["fase"] += 1
                st.session_state["desafio_atual"] = 0
                prog = buscar_progresso(st.session_state["user_id"])
                perf = buscar_perfil(st.session_state["user_id"])
                novas, cfg = verificar_e_conceder_badges(st.session_state["user_id"], perf or {}, len(prog))
                for b in novas:
                    info = cfg.get(b, {})
                    st.toast(f"🏅 {info.get('emoji','')} {info.get('nome','')}", icon="🎉")

            if subiu:
                st.balloons()
                st.success(f"🎉 Nível {novo_nivel}!")

            import time; time.sleep(1.2)
            st.rerun()

        else:
            if not is_admin:
                st.session_state["vidas"] -= 1
                atualizar_vidas(st.session_state["user_id"], st.session_state["vidas"])

            vidas_r = st.session_state["vidas"]
            gemini_badge = '<div class="gemini-badge">✨ Avaliado por IA</div>' if fonte == "gemini" else ""

            st.markdown(f"""
            <div class="feedback-erro">
                {gemini_badge}
                <div style="color:#f87171;font-weight:700;">❌ Resposta incorreta</div>
                {'<div style="color:#fca5a5;margin-top:6px;font-size:0.9rem;">'+feedback+'</div>' if feedback and fonte=='gemini' else ''}
                {'<div style="color:#9b9ba8;margin-top:8px;font-size:0.82rem;">❤️ '+str(vidas_r)+' vidas restantes</div>' if not is_admin else ''}
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🧑‍🏫 Ver explicação do professor"):
                st.markdown(f"""
                <div class="professor-box">
                    <div style="margin-bottom:10px;"><span style="color:#fbbf24;font-weight:700;">💡 Dica:</span> <span style="color:#d4d3cc;">{desafio.get('dica','')}</span></div>
                    <div style="margin-bottom:10px;"><span style="color:#f87171;font-weight:700;">⚠️ Erro comum:</span> <span style="color:#d4d3cc;">{desafio.get('erro_comum','')}</span></div>
                    <div style="margin-bottom:10px;"><span style="color:#4ade80;font-weight:700;">📘 Explicação:</span> <span style="color:#d4d3cc;">{desafio.get('explicacao','')}</span></div>
                    <div><span style="color:#a78bfa;font-weight:700;">🧠 Lógica:</span> <span style="color:#d4d3cc;font-family:'DM Mono',monospace;font-size:0.85rem;">{desafio.get('logica','')}</span></div>
                </div>
                """, unsafe_allow_html=True)
