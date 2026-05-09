# Tema global do CodeQuest — importado em todas as páginas
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:        #111318;
    --surface:   #1c1f27;
    --surface2:  #252833;
    --border:    #2e3240;
    --border2:   #3a3f52;
    --text:      #f4f3ee;
    --text2:     #b0b3c1;
    --text3:     #7a7d8e;
    --accent:    #7c6af7;
    --accent2:   #a78bfa;
    --green:     #3ddc84;
    --red:       #f4645f;
    --yellow:    #fbbf24;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

/* Esconde sidebar e nav lateral do Streamlit */
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu                        { display: none !important; }
footer                           { display: none !important; }
header                           { display: none !important; }

/* Inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"]  textarea {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    caret-color: var(--accent) !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"]  textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,106,247,0.18) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"]  label {
    color: var(--text2) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
}

/* Botões */
.stButton button {
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    transition: all 0.18s ease !important;
}
.stButton button[kind="primary"] {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
}
.stButton button[kind="primary"]:hover {
    background: var(--accent2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(124,106,247,0.35) !important;
}
.stButton button[kind="secondary"] {
    background: var(--surface2) !important;
    color: var(--text2) !important;
    border: 1.5px solid var(--border2) !important;
}
.stButton button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--text) !important;
}

/* Expander */
details {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
}
details summary { color: var(--text2) !important; font-weight: 600 !important; }

/* Alertas */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* Code blocks */
pre, code {
    font-family: 'DM Mono', monospace !important;
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 0.85rem !important;
}
</style>
"""
