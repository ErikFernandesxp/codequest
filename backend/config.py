# ═══════════════════════════════════════════════════════════════
#  CodeQuest — Arquivo de Configuração Central
#  Edite aqui para mudar cores, textos e comportamentos do jogo
# ═══════════════════════════════════════════════════════════════

# ── TEMA DE CORES ────────────────────────────────────────────────
# Para mudar o tema, altere os valores abaixo.
# Exemplo: mudar para tema claro, troque BG para "#ffffff"

CORES = {
    # Fundos
    "bg":           "#0f1117",   # Fundo principal
    "surface":      "#1a1d26",   # Cards
    "surface2":     "#232734",   # Elementos secundários

    # Bordas
    "border":       "#2f3545",
    "border2":      "#facc15",

    # Textos
    "text":         "#f8fafc",
    "text2":        "#cbd5e1",
    "text3":        "#94a3b8",

    # Destaque (AMARELO/DOURADO)
    "accent":       "#facc15",   # Amarelo principal
    "accent2":      "#f59e0b",   # Dourado/laranja

    # Feedback
    "green":        "#22c55e",
    "red":          "#ef4444",
    "yellow":       "#facc15",
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
