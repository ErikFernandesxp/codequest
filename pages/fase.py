import streamlit as st

st.set_page_config(page_title="CodeQuest", page_icon="🎯", layout="wide",
                   initial_sidebar_state="collapsed")

import json, os, time
from backend.session import init_session, calcular_nivel
from backend.gemini_validator import validar_resposta
from backend.crud import (salvar_progresso, atualizar_xp_nivel,
                           calcular_vidas_regeneradas, atualizar_vidas,
                           buscar_perfil, verificar_e_conceder_badges,
                           buscar_progresso)
from backend.theme import CSS

init_session(st)
if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

st.markdown(CSS, unsafe_allow_html=True)
st.markdown("""
<style>
/* Topbar */
.topbar {
    display:flex; align-items:center; justify-content:space-between;
    padding:12px 24px; background:#1c1f27;
    border-bottom:1.5px solid #2e3240;
    margin-bottom:20px; border-radius:0 0 14px 14px;
}
.tb-logo { font-size:1.1rem; font-weight:800; color:#f4f3ee; }
.tb-logo span { color:#7c6af7; }
.tb-lang {
    background:#252833; border:1px solid #2e3240;
    padding:4px 12px; border-radius:20px;
    font-size:0.78rem; color:#b0b3c1;
    font-family:'DM Mono',monospace;
}
.tb-stats { display:flex; gap:10px; }
.tb-pill {
    background:#252833; border:1px solid #2e3240;
    padding:5px 13px; border-radius:20px;
    font-size:0.82rem; font-weight:600; color:#f4f3ee;
}

/* Fase header */
.fase-card {
    background:#1c1f27; border:1.5px solid #2e3240;
    border-radius:16px; padding:20px 24px; margin-bottom:18px;
}
.fase-titulo { font-size:1.25rem; font-weight:800; color:#f4f3ee; margin-bottom:4px; }
.fase-sub    { font-size:0.8rem; color:#b0b3c1; }
.prog-bg   { background:#252833; border-radius:4px; height:6px; margin-top:12px; }
.prog-fill { background:linear-gradient(90deg,#7c6af7,#a78bfa); height:6px; border-radius:4px; }

/* Info boxes */
.box-conceito {
    background:#1c1f27; border:1.5px solid #2e3240;
    border-left:3px solid #7c6af7;
    border-radius:12px; padding:14px 18px; margin-bottom:10px;
}
.box-dica {
    background:#0d1f16; border:1.5px solid #1a3a26;
    border-left:3px solid #3ddc84;
    border-radius:12px; padding:14px 18px;
}
.box-label {
    font-size:0.68rem; font-weight:700; text-transform:uppercase;
    letter-spacing:1px; margin-bottom:6px;
}
.box-text { font-size:0.87rem; color:#d4d3cc; line-height:1.6; }

/* Pergunta */
.pergunta-card {
    background:#111318; border:2px solid #2e3240;
    border-radius:14px; padding:22px 24px; margin:16px 0;
}
.perg-label { font-size:0.68rem; color:#7c6af7; font-weight:700;
              text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }
.perg-texto { font-size:1.05rem; font-weight:600; color:#f4f3ee; line-height:1.55; }

/* Feedback */
.fb-ok  { background:#0d2416; border:1.5px solid #166534;
          border-radius:12px; padding:16px 20px; margin-top:14px; }
.fb-err { background:#1f0a0a; border:1.5px solid #7f1d1d;
          border-radius:12px; padding:16px 20px; margin-top:14px; }
.fb-title-ok  { color:#3ddc84; font-weight:700; font-size:1rem; }
.fb-title-err { color:#f4645f; font-weight:700; font-size:1rem; }
.fb-body { font-size:0.88rem; margin-top:6px; line-height:1.5; }

/* Professor */
.prof-box {
    background:#1a1824; border:1.5px solid #2a2747;
    border-radius:12px; padding:18px 20px;
}
.prof-row { margin-bottom:10px; font-size:0.88rem; line-height:1.5; }
.prof-label { font-weight:700; margin-right:4px; }

/* Gemini badge */
.ai-badge {
    display:inline-flex; align-items:center; gap:5px;
    background:#0c1a30; border:1px solid #1e3a6e;
    border-radius:20px; padding:3px 10px;
    font-size:0.7rem; color:#60a5fa; font-weight:700;
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

is_admin = st.session_state.get("is_admin", False)

if not st.session_state.get("vidas_sincronizadas") and not is_admin:
    p = buscar_perfil(st.session_state["user_id"])
    if p:
        vn = calcular_vidas_regeneradas(p.get("ultima_vida",""), p.get("vidas",3))
        st.session_state["vidas"] = vn
        st.session_state["vidas_sincronizadas"] = True

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
ling          = st.session_state.get("linguagem")
fase_idx      = st.session_state.get("fase", 0)
lang_icons    = {"python":"🐍","c":"⚙️","java":"☕","php":"🌐"}

if not ling or ling not in fases:
    st.error("Linguagem inválida.")
    if st.button("← Escolher linguagem"):
        st.switch_page("pages/linguagem.py")
    st.stop()

vidas_disp  = "∞" if is_admin else st.session_state["vidas"]
xp          = st.session_state["xp"]
nivel       = st.session_state["nivel"]
streak      = st.session_state.get("streak", 0)
total_fases = len(fases[ling])

# ── Topbar ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div style="display:flex;align-items:center;gap:14px;">
    <div class="tb-logo">Code<span>Quest</span></div>
    <div class="tb-lang">{lang_icons.get(ling,'')} {ling.upper()} · Fase {fase_idx+1}/{total_fases}</div>
  </div>
  <div class="tb-stats">
    <div class="tb-pill">❤️ {vidas_disp}</div>
    <div class="tb-pill">⚡ {xp} XP</div>
    <div class="tb-pill">🏆 Nv.{nivel}</div>
    <div class="tb-pill">🔥 {streak}d</div>
  </div>
</div>
""", unsafe_allow_html=True)

cn1, cn2, _ = st.columns([1, 1, 8])
with cn1:
    if st.button("🏠 Menu"):
        st.session_state["vidas_sincronizadas"] = False
        st.switch_page("pages/dashboard.py")
with cn2:
    if st.button("📚 Trilhas"):
        st.switch_page("pages/linguagem.py")

# ── Game Over ─────────────────────────────────────────────────────────────────
if not is_admin and st.session_state["vidas"] <= 0:
    st.markdown("""
    <div style="text-align:center;padding:60px 0;">
      <div style="font-size:4rem;">💀</div>
      <h2 style="color:#f4f3ee;">Game Over</h2>
      <p style="color:#b0b3c1;">Suas vidas regeneram 1 a cada 30 minutos.</p>
    </div>""", unsafe_allow_html=True)
    if st.button("🏠 Voltar ao Menu", use_container_width=True):
        st.session_state["vidas_sincronizadas"] = False
        st.switch_page("pages/dashboard.py")
    st.stop()

# ── Fim da trilha ─────────────────────────────────────────────────────────────
if fase_idx >= len(fases[ling]):
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center;padding:60px 0;">
      <div style="font-size:4rem;">🏆</div>
      <h2 style="color:#f4f3ee;">Trilha concluída!</h2>
      <p style="color:#b0b3c1;">Você finalizou todas as fases de {ling.upper()}!</p>
      <p style="color:#7c6af7;font-size:1.2rem;font-weight:700;">⚡ {xp} XP acumulados</p>
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 Outra linguagem", use_container_width=True, type="primary"):
            st.session_state["vidas_sincronizadas"] = False
            st.switch_page("pages/linguagem.py")
    with c2:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.update({"fase":0,"desafio_atual":0})
            st.rerun()
    st.stop()

fase = fases[ling][fase_idx]
if not isinstance(fase, dict) or "desafios" not in fase:
    st.error("Erro nos dados da fase.")
    st.stop()

desafios = fase["desafios"]
idx      = st.session_state.get("desafio_atual", 0)
if idx >= len(desafios):
    st.session_state["desafio_atual"] = 0
    st.rerun()

desafio = desafios[idx]
if isinstance(desafio, str):
    desafio = {"pergunta":desafio,"resposta":"","dica":"","erro_comum":"","explicacao":"","logica":""}

pct_fase = int(((idx+1)/len(desafios))*100)

# ── Fase header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="fase-card">
  <div class="fase-titulo">🎯 {fase.get('titulo','')}</div>
  <div class="fase-sub">Desafio {idx+1} de {len(desafios)}</div>
  <div class="prog-bg"><div class="prog-fill" style="width:{pct_fase}%"></div></div>
</div>
""", unsafe_allow_html=True)

# ── Conteúdo ──────────────────────────────────────────────────────────────────
col_l, col_r = st.columns([1, 1])

with col_l:
    st.markdown(f"""
    <div class="box-conceito">
      <div class="box-label" style="color:#7c6af7;">📖 Conceito</div>
      <div class="box-text">{fase.get('explicacao','')}</div>
    </div>
    <div class="box-dica">
      <div class="box-label" style="color:#3ddc84;">💡 Dica</div>
      <div class="box-text">{desafio.get('dica','')}</div>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    st.markdown("<div style='font-size:0.68rem;color:#b0b3c1;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>📌 Exemplo</div>", unsafe_allow_html=True)
    st.code(fase.get("exemplo",""), language=ling)

# ── Pergunta ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="pergunta-card">
  <div class="perg-label">🧩 Desafio {idx+1}</div>
  <div class="perg-texto">{desafio.get('pergunta','')}</div>
</div>
""", unsafe_allow_html=True)

resposta = st.text_area("💻 Seu código:", height=130,
                         key=f"inp_{fase_idx}_{idx}",
                         placeholder="Digite sua resposta aqui...")

cb1, cb2, cb3, _ = st.columns([1,1,1,3])
enviar = cb1.button("🚀 Enviar", type="primary", use_container_width=True)
pular  = cb2.button("⏭️ Pular" + ("" if is_admin else " -1❤️"), use_container_width=True)
voltar = cb3.button("🏠 Menu", use_container_width=True)

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
                pergunta=desafio.get("pergunta",""),
                resposta_aluno=resposta,
                linguagem=ling,
                gabarito=desafio.get("resposta",""),
                respostas_aceitas=desafio.get("respostas_aceitas",[]),
                keywords=desafio.get("keywords",[])
            )

        ai_badge = '<div class="ai-badge">✨ Avaliado por IA</div>' if fonte=="gemini" else ""

        if correto:
            fb_txt = feedback if (feedback and feedback not in ["Correto!",""]) else "Solução perfeita! Continue assim."
            st.markdown(f"""
            <div class="fb-ok">
              {ai_badge}
              <div class="fb-title-ok">✅ Correto! Muito bem!</div>
              <div class="fb-body" style="color:#86efac;">{fb_txt}</div>
            </div>""", unsafe_allow_html=True)

            novo_xp    = xp + 10
            novo_nivel = calcular_nivel(novo_xp)
            subiu      = novo_nivel > nivel
            st.session_state.update({"xp":novo_xp,"nivel":novo_nivel})
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
                novas, cfg = verificar_e_conceder_badges(
                    st.session_state["user_id"], perf or {}, len(prog))
                for b in novas:
                    info = cfg.get(b,{})
                    st.toast(f"🏅 {info.get('emoji','')} {info.get('nome','')}", icon="🎉")

            if subiu:
                st.balloons()
                st.success(f"🎉 Subiu para o Nível {novo_nivel}!")

            time.sleep(1.2)
            st.rerun()

        else:
            if not is_admin:
                st.session_state["vidas"] -= 1
                atualizar_vidas(st.session_state["user_id"], st.session_state["vidas"])

            vr = st.session_state["vidas"]
            fb_txt = feedback if (feedback and fonte=="gemini") else ""
            vidas_info = f'<div style="color:#b0b3c1;font-size:0.8rem;margin-top:8px;">❤️ {vr} vidas restantes</div>' if not is_admin else ""

            st.markdown(f"""
            <div class="fb-err">
              {ai_badge}
              <div class="fb-title-err">❌ Resposta incorreta</div>
              {'<div class="fb-body" style="color:#fca5a5;">'+fb_txt+'</div>' if fb_txt else ''}
              {vidas_info}
            </div>""", unsafe_allow_html=True)

            with st.expander("🧑‍🏫 Ver explicação do professor"):
                st.markdown(f"""
                <div class="prof-box">
                  <div class="prof-row"><span class="prof-label" style="color:#fbbf24;">💡 Dica:</span> <span style="color:#d4d3cc;">{desafio.get('dica','')}</span></div>
                  <div class="prof-row"><span class="prof-label" style="color:#f4645f;">⚠️ Erro comum:</span> <span style="color:#d4d3cc;">{desafio.get('erro_comum','')}</span></div>
                  <div class="prof-row"><span class="prof-label" style="color:#3ddc84;">📘 Explicação:</span> <span style="color:#d4d3cc;">{desafio.get('explicacao','')}</span></div>
                  <div class="prof-row"><span class="prof-label" style="color:#a78bfa;">🧠 Lógica:</span> <span style="color:#d4d3cc;font-family:'DM Mono',monospace;font-size:0.82rem;">{desafio.get('logica','')}</span></div>
                </div>
                """, unsafe_allow_html=True)
