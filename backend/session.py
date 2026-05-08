# Email do dono do sistema — vida infinita!
ADMIN_EMAIL = "erikfernandescamisa8@gmail.com"

def init_session(st):
    defaults = {
        "logado": False,
        "usuario": None,
        "user_id": None,
        "usuario_email": None,
        "linguagem": None,
        "fase": 0,
        "desafio_atual": 0,
        "xp": 0,
        "nivel": 1,
        "vidas": 3,
        "streak": 0,
        "vidas_sincronizadas": False,
        "is_admin": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def calcular_nivel(xp: int) -> int:
    """Sobe de nível a cada 50 XP."""
    return max(1, xp // 50 + 1)


def verificar_admin(email: str) -> bool:
    """Retorna True se o email for do dono."""
    return email.strip().lower() == ADMIN_EMAIL.strip().lower()
