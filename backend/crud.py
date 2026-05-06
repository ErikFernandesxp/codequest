from backend.supabase_client import supabase


# ─── AUTH (Supabase Authentication) ─────────────────────────────────────────

def registrar_usuario(nome: str, email: str, senha: str):
    """Cria conta no Supabase Auth e salva nome na tabela users."""
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": senha,
            "options": {"data": {"nome": nome}}
        })
        if res.user:
            # Salva nome/xp/nivel na tabela users vinculado ao uid do Auth
            supabase.table("users").upsert({
                "id": res.user.id,
                "email": email,
                "nome": nome,
                "xp": 0,
                "nivel": 1
            }).execute()
            return res.user, None
        return None, "Erro ao criar conta."
    except Exception as e:
        msg = str(e)
        if "already registered" in msg:
            return None, "Este email já está cadastrado."
        return None, msg


def login_usuario(email: str, senha: str):
    """Autentica via Supabase Auth. Retorna (user, session, erro)."""
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha
        })
        if res.user and res.session:
            return res.user, res.session, None
        return None, None, "Email ou senha incorretos."
    except Exception as e:
        return None, None, "Email ou senha incorretos."


def logout_usuario():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass


def buscar_perfil(user_id: str):
    """Busca nome, xp e nivel da tabela users."""
    res = supabase.table("users").select("*").eq("id", user_id).execute()
    return res.data[0] if res.data else None


def atualizar_xp_nivel(user_id: str, xp: int, nivel: int):
    supabase.table("users").update({
        "xp": xp,
        "nivel": nivel
    }).eq("id", user_id).execute()


# ─── PROGRESSO ───────────────────────────────────────────────────────────────

def salvar_progresso(user_id: str, linguagem: str, fase: int):
    supabase.table("progress").upsert({
        "user_id": user_id,
        "linguagem": linguagem,
        "fase": fase,
        "concluido": True
    }, on_conflict="user_id,linguagem,fase").execute()


def buscar_progresso(user_id: str):
    res = supabase.table("progress").select("*").eq("user_id", user_id).execute()
    return res.data or []


def fases_concluidas(user_id: str, linguagem: str):
    dados = buscar_progresso(user_id)
    return {d["fase"] for d in dados if d["linguagem"] == linguagem}
