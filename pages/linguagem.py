import streamlit as st

st.set_page_config(page_title="CodeQuest — Trilhas", page_icon="🎮", layout="wide",
                   initial_sidebar_state="collapsed")

import json, os
from backend.session import init_session
from backend.crud import buscar_progresso
from backend.theme import CSS

init_session(st)
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
}
.nav-logo { font-size:1.35rem; font-weight:800; color:#f4f3ee; }
.nav-logo span { color:#7c6af7; }

.lang-card {
    background:#1c1f27; border:2px solid #2e3240;
    border-radius:18px; padding:26px 20px;
    text-align:center; transition:all 0.2s;
}
.lang-card:hover { border-color:#7c6af7; transform:translateY(-3px);
    box-shadow:0 8px 24px rgba(124,106,247,0.15); }
.lang-icon  { font-size:3rem; margin-bottom:10px; }
.lang-title { font-size:1.15rem; font-weight:800; color:#f4f3ee; }
.lang-desc  { font-size:0.8rem; color:#b0b3c1; margin:6px 0 14px; line-height:1.5; }
.level-badge {
    display:inline-block; padding:4px 14px; border-radius:20px;
    font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;
}
.lv-init { background:#0d2416; color:#3ddc84; border:1px solid #166534; }
.lv-mid  { background:#0c1a30; color:#60a5fa; border:1px solid #1e3a6e; }
.lv-adv  { background:#2a0a0a; color:#f4645f; border:1px solid #7f1d1d; }

.bar-bg   { background:#252833; border-radius:4px; height:5px; margin-top:10px; }
.bar-fill { background:linear-gradient(90deg,#7c6af7,#a78bfa); height:5px; border-radius:4px; }
.done-badge {
    display:inline-block; background:#0d2416; color:#3ddc84;
    border:1px solid #166534; border-radius:8px;
    padding:6px 14px; font-size:0.8rem; font-weight:700;
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def fases_json():
    with open(os.path.join(os.getcwd(),"data","fases.json"), encoding="utf-8") as f:
        return json.load(f)

fases     = fases_json()
progresso = buscar_progresso(st.session_state["user_id"])
concluidas = {}
for p in progresso:
    concluidas[p["linguagem"]] = concluidas.get(p["linguagem"],0) + 1

st.markdown("""
<div class="navbar">
  <div class="nav-logo">Code<span>Quest</span></div>
</div>
""", unsafe_allow_html=True)

if st.button("← Voltar ao Menu"):
    st.switch_page("pages/dashboard.py")

st.markdown("<h2 style='font-size:1.7rem;font-weight:800;margin:16px 0 6px;color:#f4f3ee;'>Escolha sua trilha</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#b0b3c1;margin-bottom:24px;font-size:0.9rem;'>Selecione a linguagem que deseja aprender</p>", unsafe_allow_html=True)

lang_info = {
    "python": {"icon":"🐍","titulo":"Python","nivel":"lv-init","nivel_label":"Iniciante",
               "desc":"Ideal para começar. Sintaxe clara, usada em IA, dados e web."},
    "c":      {"icon":"⚙️","titulo":"C","nivel":"lv-adv","nivel_label":"Avançado",
               "desc":"Base da computação. Ponteiros, memória e alta performance."},
    "java":   {"icon":"☕","titulo":"Java","nivel":"lv-mid","nivel_label":"Intermediário",
               "desc":"Orientação a objetos, Android e sistemas corporativos."},
    "php":    {"icon":"🌐","titulo":"PHP","nivel":"lv-mid","nivel_label":"Intermediário",
               "desc":"Linguagem rainha do backend web. Usada em milhões de sites."},
}

cols = st.columns(4)
for i, (lang, info) in enumerate(lang_info.items()):
    total  = len(fases.get(lang,[]))
    feitas = concluidas.get(lang,0)
    pct    = int(feitas/total*100) if total else 0
    fases_feitas = {p["fase"] for p in progresso if p["linguagem"] == lang}
    proxima = next((j for j in range(total) if j not in fases_feitas), total)

    with cols[i]:
        st.markdown(f"""
        <div class="lang-card">
          <div class="lang-icon">{info['icon']}</div>
          <div class="lang-title">{info['titulo']}</div>
          <div class="lang-desc">{info['desc']}</div>
          <div class="level-badge {info['nivel']}">{info['nivel_label']}</div>
          <div style="font-size:0.78rem;color:#b0b3c1;margin-top:12px;">{feitas}/{total} fases &nbsp;·&nbsp; {pct}%</div>
          <div class="bar-bg"><div class="bar-fill" style="width:{pct}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if feitas >= total and total > 0:
            st.markdown('<div class="done-badge">✅ Trilha concluída!</div>', unsafe_allow_html=True)
            if st.button("🔄 Repetir", key=f"rep_{lang}", use_container_width=True):
                st.session_state.update({"linguagem":lang,"fase":0,"desafio_atual":0,"vidas_sincronizadas":False})
                st.switch_page("pages/fase.py")
        elif feitas > 0 and proxima < total:
            if st.button(f"▶️ Continuar", key=f"cont_{lang}", use_container_width=True, type="primary"):
                st.session_state.update({"linguagem":lang,"fase":proxima,"desafio_atual":0,"vidas_sincronizadas":False})
                st.switch_page("pages/fase.py")
            if st.button("↩️ Do início", key=f"inicio_{lang}", use_container_width=True):
                st.session_state.update({"linguagem":lang,"fase":0,"desafio_atual":0,"vidas_sincronizadas":False})
                st.switch_page("pages/fase.py")
        else:
            if st.button(f"🚀 Começar", key=f"start_{lang}", use_container_width=True, type="primary"):
                st.session_state.update({"linguagem":lang,"fase":0,"desafio_atual":0,"vidas_sincronizadas":False})
                st.switch_page("pages/fase.py")
