import streamlit as st

st.set_page_config(page_title="CodeQuest", page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

import json, os
from backend.session import init_session
from backend.crud import buscar_progresso

init_session(st)

if not st.session_state.get("logado"):
    st.switch_page("pages/login.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&display=swap');
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

.lang-card {
    background: #16161d; border: 2px solid #2a2a35;
    border-radius: 20px; padding: 28px 24px;
    cursor: pointer; transition: all 0.2s;
    text-align: center; height: 100%;
}
.lang-card:hover { border-color: #7c6af7; transform: translateY(-2px); }
.lang-icon-big { font-size: 3rem; margin-bottom: 12px; }
.lang-title { font-size: 1.3rem; font-weight: 800; color: #f0efe8; }
.lang-desc { font-size: 0.82rem; color: #9b9ba8; margin: 6px 0 14px 0; line-height: 1.4; }
.lang-badge {
    display: inline-block; padding: 4px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
}
.badge-iniciante { background: #1a2e1a; color: #4ade80; }
.badge-intermediario { background: #1a1f2e; color: #60a5fa; }
.badge-avancado { background: #2e1a1a; color: #f87171; }

.prog-bar-bg { background: #2a2a35; border-radius: 3px; height: 4px; margin-top: 10px; }
.prog-bar-fill { background: linear-gradient(90deg,#7c6af7,#a78bfa); height: 4px; border-radius: 3px; }

.stButton button {
    border-radius: 12px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_fases():
    with open(os.path.join(os.getcwd(),"data","fases.json"), encoding="utf-8") as f:
        return json.load(f)

fases = carregar_fases()
progresso = buscar_progresso(st.session_state["user_id"])
concluidas = {}
for p in progresso:
    concluidas[p["linguagem"]] = concluidas.get(p["linguagem"],0) + 1

# ─── Navbar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Code<span>Quest</span></div>
</div>
""", unsafe_allow_html=True)

if st.button("← Voltar ao Menu"):
    st.switch_page("pages/dashboard.py")

st.markdown("<h2 style='font-size:1.8rem;font-weight:800;margin:20px 0 8px;'>Escolha sua trilha</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#9b9ba8;margin-bottom:28px;'>Selecione a linguagem que deseja aprender ou continuar</p>", unsafe_allow_html=True)

lang_info = {
    "python": {
        "icon":"🐍","titulo":"Python","nivel":"iniciante",
        "desc":"Ideal para começar. Sintaxe simples e muito usada em IA, dados e web."
    },
    "c": {
        "icon":"⚙️","titulo":"C","nivel":"avancado",
        "desc":"Fundamentos da computação. Ponteiros, memória e alta performance."
    },
    "java": {
        "icon":"☕","titulo":"Java","nivel":"intermediario",
        "desc":"Orientação a objetos, Android e sistemas corporativos."
    },
    "php": {
        "icon":"🌐","titulo":"PHP","nivel":"intermediario",
        "desc":"Linguagem rainha do backend web. Usada em 80% dos sites."
    },
}

cols = st.columns(4)
for i, (lang, info) in enumerate(lang_info.items()):
    total = len(fases.get(lang,[]))
    feitas = concluidas.get(lang,0)
    pct = int(feitas/total*100) if total else 0
    fases_feitas = {p["fase"] for p in progresso if p["linguagem"] == lang}
    proxima = next((j for j in range(total) if j not in fases_feitas), total)

    with cols[i]:
        st.markdown(f"""
        <div class="lang-card">
            <div class="lang-icon-big">{info['icon']}</div>
            <div class="lang-title">{info['titulo']}</div>
            <div class="lang-desc">{info['desc']}</div>
            <div class="lang-badge badge-{info['nivel']}">
                {'Iniciante' if info['nivel']=='iniciante' else 'Intermediário' if info['nivel']=='intermediario' else 'Avançado'}
            </div>
            <div style="font-size:0.78rem;color:#9b9ba8;margin-top:12px;">{feitas}/{total} fases · {pct}%</div>
            <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{pct}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if feitas > 0 and proxima < total:
            if st.button(f"▶️ Continuar", key=f"cont_{lang}", use_container_width=True, type="primary"):
                st.session_state.update({"linguagem":lang,"fase":proxima,"desafio_atual":0,"vidas_sincronizadas":False})
                st.switch_page("pages/fase.py")
            if st.button(f"↩️ Do início", key=f"inicio_{lang}", use_container_width=True):
                st.session_state.update({"linguagem":lang,"fase":0,"desafio_atual":0,"vidas_sincronizadas":False})
                st.switch_page("pages/fase.py")
        elif feitas >= total and total > 0:
            st.success("✅ Completo!")
            if st.button("🔄 Repetir", key=f"rep_{lang}", use_container_width=True):
                st.session_state.update({"linguagem":lang,"fase":0,"desafio_atual":0,"vidas_sincronizadas":False})
                st.switch_page("pages/fase.py")
        else:
            if st.button(f"🚀 Começar", key=f"start_{lang}", use_container_width=True, type="primary"):
                st.session_state.update({"linguagem":lang,"fase":0,"desafio_atual":0,"vidas_sincronizadas":False})
                st.switch_page("pages/fase.py")
