# ═══════════════════════════════════════════════════════════════
#  CodeQuest — Arquivo de Configuração Central
#  Edite aqui para mudar cores, textos e comportamentos do jogo
# ═══════════════════════════════════════════════════════════════

# ── TEMA DE CORES ────────────────────────────────────────────────
# Para mudar o tema, altere os valores abaixo.
# Exemplo: mudar para tema claro, troque BG para "#ffffff"

CORES = {
    # Fundos
    "bg":           "#FFFFFF",   # Fundo principal da página
    "surface":      "#1c1f27",   # Cards e painéis
    "surface2":     "#252833",   # Inputs e elementos secundários

    # Bordas
    "border":       "#2e3240",   # Borda padrão
    "border2":      "#3a3f52",   # Borda de foco

    # Textos
    "text":         "#f4f3ee",   # Texto principal
    "text2":        "#b0b3c1",   # Texto secundário
    "text3":        "#7a7d8e",   # Texto apagado/hint

    # Cores de destaque
    "accent":       "#7c6af7",   # Roxo principal (botões, links)
    "accent2":      "#a78bfa",   # Roxo claro (hover, gradientes)

    # Cores de feedback
    "green":        "#3ddc84",   # Resposta correta
    "red":          "#f4645f",   # Resposta incorreta / erro
    "yellow":       "#fbbf24",   # Streak / avisos
}

# ── EXEMPLO: TEMA CLARO ──────────────────────────────────────────
# Para ativar tema claro, descomente e substitua o CORES acima:
#
# CORES = {
#     "bg":           "#f8f9fa",
#     "surface":      "#ffffff",
#     "surface2":     "#f1f3f5",
#     "border":       "#dee2e6",
#     "border2":      "#adb5bd",
#     "text":         "#212529",
#     "text2":        "#495057",
#     "text3":        "#868e96",
#     "accent":       "#7c6af7",
#     "accent2":      "#a78bfa",
#     "green":        "#2f9e44",
#     "red":          "#e03131",
#     "yellow":       "#f08c00",
# }

# ── CONFIGURAÇÕES DO JOGO ────────────────────────────────────────
JOGO = {
    "xp_por_acerto":        10,    # XP ganho por resposta certa
    "vidas_iniciais":       3,     # Vidas que o jogador começa
    "minutos_regenerar_vida": 30,  # Minutos para regenerar 1 vida
    "xp_por_nivel":         50,    # XP necessário para subir de nível
    "streak_minimo_exibir": 2,     # Dias mínimos para mostrar streak
}

# ── LINGUAGENS DISPONÍVEIS ───────────────────────────────────────
LINGUAGENS = {
    "Python": {"chave": "python", "icone": "🐍"},
    "C":      {"chave": "c",      "icone": "⚙️"},
    "Java":   {"chave": "java",   "icone": "☕"},
    "PHP":    {"chave": "php",    "icone": "🌐"},
}

# ── TEXTOS DA INTERFACE ──────────────────────────────────────────
TEXTOS = {
    "nome_app":     "CodeQuest",
    "tagline":      "Aprenda programação jogando",
    "btn_jogar":    "🚀 Jogar — Escolher Linguagem",
    "btn_ranking":  "🏆 Ranking",
    "btn_sair":     "🚪 Sair",
    "btn_enviar":   "🚀 Enviar",
    "btn_pular":    "⏭️ Pular",
    "btn_menu":     "🏠 Menu",
}
