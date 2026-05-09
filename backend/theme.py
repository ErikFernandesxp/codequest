# Tema global do CodeQuest — gerado a partir do config.py
# NÃO edite as cores aqui, edite em backend/config.py

from backend.config import CORES

def gerar_css():
    c = CORES
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

:root {{
    --bg:      {c['bg']};
    --surface: {c['surface']};
    --surface2:{c['surface2']};
    --border:  {c['border']};
    --border2: {c['border2']};
    --text:    {c['text']};
    --text2:   {c['text2']};
    --text3:   {c['text3']};
    --accent:  {c['accent']};
    --accent2: {c['accent2']};
    --green:   {c['green']};
    --red:     {c['red']};
    --yellow:  {c['yellow']};
}}

html, body, [class*="css"] {{
    font-family: 'Syne', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}}
.stApp {{ background: var(--bg) !important; }}

[data-testid="stSidebar"]        {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}
#MainMenu                        {{ display: none !important; }}
footer                           {{ display: none !important; }}
header                           {{ display: none !important; }}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"]  textarea {{
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    caret-color: var(--accent) !important;
    -webkit-text-fill-color: var(--text) !important;
}}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"]  textarea::placeholder {{
    color: var(--text3) !important;
    opacity: 1 !important;
    -webkit-text-fill-color: var(--text3) !important;
}}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"]  textarea:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,106,247,0.18) !important;
    outline: none !important;
}}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"]  label {{
    color: var(--text2) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}}

input, textarea, select {{
    -webkit-appearance: none !important;
    background-color: var(--surface2) !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}}
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {{
    -webkit-box-shadow: 0 0 0px 1000px {c['surface2']} inset !important;
    -webkit-text-fill-color: {c['text']} !important;
}}

.stButton button {{
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    transition: all 0.18s ease !important;
}}
.stButton button[kind="primary"] {{
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
}}
.stButton button[kind="primary"]:hover {{
    background: var(--accent2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(124,106,247,0.35) !important;
}}
.stButton button[kind="secondary"] {{
    background: var(--surface2) !important;
    color: var(--text2) !important;
    border: 1.5px solid var(--border2) !important;
}}
.stButton button[kind="secondary"]:hover {{
    border-color: var(--accent) !important;
    color: var(--text) !important;
}}

details {{
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
}}
details summary {{ color: var(--text2) !important; font-weight: 600 !important; }}

div[data-testid="stAlert"] {{
    border-radius: 10px !important;
    font-weight: 500 !important;
}}

pre, code {{
    font-family: 'DM Mono', monospace !important;
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 0.85rem !important;
}}

@media (max-width: 768px) {{
    .stButton button {{ font-size: 0.85rem !important; }}
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"]  textarea {{ font-size: 1rem !important; }}
}}
</style>
"""

# CSS é gerado dinamicamente a partir das cores do config.py
CSS = gerar_css()
