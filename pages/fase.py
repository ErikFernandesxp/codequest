import streamlit as st

st.set_page_config(page_title="CodeQuest - Fase", page_icon="🎯", layout="wide")

import json
import os
from backend.session import init_session, calcular_nivel
from backend.validator import validar_codigo
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

# Sincroniza vidas com banco ao entrar na fase (só para não-admin)
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

if not ling or ling not in fases:
    st.error("❌ Linguagem inválida. Volte e escolha uma linguagem.")
    if st.button("← Escolher linguagem"):
        st.switch_page("pages/linguagem.py")
    st.stop()

# ─── Sidebar HUD ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['usuario']}")
    if is_admin:
        st.markdown("👑 **Admin**")
    st.metric("⚡ XP", st.session_state["xp"])
    st.metric("🏆 Nível", st.session_state["nivel"])
    xp_mod = st.session_state["xp"] % 50
    st.progress(xp_mod / 50, text=f"XP para próx. nível: {xp_mod}/50")

    if is_admin:
        st.metric("❤️ Vidas", "∞")
    else:
        st.metric("❤️ Vidas", st.session_state["vidas"])

    st.metric("🔥 Dias seguidos", f"{st.session_state.get('streak', 0)} dias")
    st.divider()

    lang_icons = {"python": "🐍", "c": "⚙️", "java": "☕", "php": "🌐"}
    total = len(fases[ling])
    st.progress(fase_idx / total if total else 0,
                text=f"{lang_icons.get(ling, '')} {ling.upper()}: fase {fase_idx + 1}/{total}")
    st.divider()

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state["vidas_sincronizadas"] = False
        st.switch_page("pages/dashboard.py")

# ─── Game Over (só para não-admin) ───────────────────────────────────────────
if not is_admin and st.session_state["vidas"] <= 0:
    st.error("💀 Game Over! Você ficou sem vidas.")
    st.info("❤️ Suas vidas regeneram 1 a cada 30 minutos. Volte mais tarde!")
    if st.button("🏠 Voltar ao Menu"):
        st.session_state["vidas_sincronizadas"] = False
        st.switch_page("pages/dashboard.py")
    st.stop()

# ─── Fim do jogo ─────────────────────────────────────────────────────────────
if fase_idx >= len(fases[ling]):
    st.balloons()
    st.success("🎉 Parabéns! Você finalizou todas as fases desta linguagem!")
    st.metric("⚡ XP Total", st.session_state["xp"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Escolher outra linguagem", use_container_width=True, type="primary"):
            st.session_state["vidas_sincronizadas"] = False
            st.switch_page("pages/linguagem.py")
    with col2:
        if st.button("🔄 Reiniciar trilha", use_container_width=True):
            st.session_state.update({"fase": 0, "desafio_atual": 0, "vidas_sincronizadas": False})
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

resposta = st.text_area(
    "💻 Digite seu código:",
    height=120,
    key=f"input_{fase_idx}_{idx}",
    placeholder="Escreva sua resposta aqui..."
)

col_btn1, col_btn2, col_btn3, _ = st.columns([1, 1, 1, 2])
enviar = col_btn1.button("🚀 Enviar", type="primary", use_container_width=True)
pular = col_btn2.button("⏭️ Pular (-1 ❤️)" if not is_admin else "⏭️ Pular", use_container_width=True)
voltar = col_btn3.button("🏠 Menu", use_container_width=True)

if voltar:
    st.session_state["vidas_sincronizadas"] = False
    st.switch_page("pages/dashboard.py")

if pular:
    if not is_admin:
        st.session_state["vidas"] -= 1
        atualizar_vidas(st.session_state["user_id"], st.session_state["vidas"])

    vidas_rest = st.session_state["vidas"]

    if not is_admin and vidas_rest <= 0:
        st.error("💀 Sem vidas! Game Over ao pular.")
        st.rerun()
    else:
        if is_admin:
            st.warning("⏭️ Desafio pulado!")
        else:
            st.warning(f"⏭️ Desafio pulado! Você perdeu uma vida. Restam {vidas_rest} ❤️")

        st.session_state["desafio_atual"] += 1
        if st.session_state["desafio_atual"] >= len(desafios):
            st.session_state["fase"] += 1
            st.session_state["desafio_atual"] = 0
        st.rerun()

if enviar:
    if not resposta.strip():
        st.warning("Digite algo antes de enviar!")
    else:
        respostas_aceitas = desafio.get("respostas_aceitas", [])
        keywords = desafio.get("keywords", [])
        ok, feedback = validar_codigo(
            resposta,
            desafio.get("resposta", ""),
            respostas_aceitas=respostas_aceitas,
            keywords=keywords
        )

        if ok:
            st.success("✅ Correto! Muito bem!")
            st.toast("🚀 +10 XP!")

            novo_xp = st.session_state["xp"] + 10
            novo_nivel = calcular_nivel(novo_xp)
            subiu_nivel = novo_nivel > st.session_state["nivel"]

            st.session_state["xp"] = novo_xp
            st.session_state["nivel"] = novo_nivel

            atualizar_xp_nivel(st.session_state["user_id"], novo_xp, novo_nivel)

            st.session_state["desafio_atual"] += 1

            if st.session_state["desafio_atual"] >= len(desafios):
                st.success("🏆 Fase concluída! Indo para a próxima...")
                salvar_progresso(st.session_state["user_id"], ling, fase_idx)
                st.session_state["fase"] += 1
                st.session_state["desafio_atual"] = 0

                # Verifica badges ao concluir fase
                progresso = buscar_progresso(st.session_state["user_id"])
                total_fases = len(progresso)
                perfil_atual = buscar_perfil(st.session_state["user_id"])
                novas_badges, cfg = verificar_e_conceder_badges(
                    st.session_state["user_id"],
                    perfil_atual or {},
                    total_fases
                )
                for b in novas_badges:
                    info = cfg.get(b, {})
                    st.toast(f"🏅 Badge: {info.get('emoji', '')} {info.get('nome', '')}", icon="🎉")

            if subiu_nivel:
                st.balloons()
                st.success(f"🎉 Subiu para o Nível {novo_nivel}!")

            st.rerun()

        else:
            if not is_admin:
                st.session_state["vidas"] -= 1
                atualizar_vidas(st.session_state["user_id"], st.session_state["vidas"])

            vidas_rest = st.session_state["vidas"]

            if is_admin:
                st.error("❌ Resposta incorreta! Tente novamente.")
            else:
                st.error(
                    f"❌ Resposta incorreta! "
                    f"({vidas_rest} {'vida' if vidas_rest == 1 else 'vidas'} "
                    f"restante{'s' if vidas_rest != 1 else ''})"
                )

            with st.expander("🧑‍🏫 Ver dica do professor", expanded=True):
                st.warning(f"💡 **Dica:** {desafio.get('dica', '')}")
                st.info(f"⚠️ **Erro comum:** {desafio.get('erro_comum', '')}")
                st.success(f"📘 **Explicação:** {desafio.get('explicacao', '')}")
                st.markdown(f"🧠 **Lógica:** {desafio.get('logica', '')}")
