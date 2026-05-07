from datetime import datetime, date, timezone, timedelta
from backend.supabase_client import supabase
import json, os


# ─── BADGES ──────────────────────────────────────────────────────────────────

def carregar_badges_config():
    caminho = os.path.join(os.getcwd(), "data", "badges.json")
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def verificar_e_conceder_badges(user_id: str, usuario: dict, total_fases: int, linguagem: str = None, fases_por_lang: dict = {}):
    """Verifica quais badges o usuário ganhou e atualiza no banco."""
    badges_atuais = set(usuario.get("badges") or [])
    novas_badges = []
    config = carregar_badges_config()

    streak = usuario.get("streak", 0)
    nivel = usuario.get("nivel", 1)

    # Badges de fases
    if total_fases >= 1 and "primeira_fase" not in badges_atuais:
        novas_badges.append("primeira_fase")
    if total_fases >= 5 and "cinco_fases" not in badges_atuais:
        novas_badges.append("cinco_fases")
    if total_fases >= 10 and "dez_fases" not in badges_atuais:
        novas_badges.append("dez_fases")

    # Badges de streak
    if streak >= 3 and "streak_3" not in badges_atuais:
        novas_badges.append("streak_3")
    if streak >= 7 and "streak_7" not in badges_atuais:
        novas_badges.append("streak_7")
    if streak >= 30 and "streak_30" not in badges_atuais:
        novas_badges.append("streak_30")

    # Badges de nível
    if nivel >= 5 and "nivel_5" not in badges_atuais:
        novas_badges.append("nivel_5")
    if nivel >= 10 and "nivel_10" not in badges_atuais:
        novas_badges.append("nivel_10")
    if nivel >= 20 and "nivel_20" not in badges_atuais:
        novas_badges.append("nivel_20")

    # Badges de linguagem completa — fases_por_lang é {"python": 3, "java": 2}
    import json, os
    try:
        caminho = os.path.join(os.getcwd(), "data", "fases.json")
        with open(caminho, encoding="utf-8") as f:
            todas_fases = json.load(f)
    except Exception:
        todas_fases = {}

    for lang in ["python", "c", "java", "php"]:
        total_lang = len(todas_fases.get(lang, []))
        concluidas_lang = fases_por_lang.get(lang, 0)
        badge_key = f"{lang}_completo"
        if total_lang > 0 and concluidas_lang >= total_lang and badge_key not in badges_atuais:
            novas_badges.append(badge_key)

    # Badge todas linguagens
    langs_completas = sum(
        1 for lang in ["python", "c", "java", "php"]
        if f"{lang}_completo" in badges_atuais or f"{lang}_completo" in novas_badges
    )
    if langs_completas == 4 and "todas_linguagens" not in badges_atuais:
        novas_badges.append("todas_linguagens")

    if novas_badges:
        todas = list(badges_atuais) + novas_badges
        supabase.table("users").update({"badges": todas}).eq("id", user_id).execute()

    return novas_badges, config


# ─── STREAK E VIDAS ──────────────────────────────────────────────────────────

def atualizar_streak(user_id: str, usuario: dict) -> int:
    """Atualiza o streak de dias. Retorna o streak atual."""
    hoje = date.today()
    ultimo = usuario.get("ultimo_acesso")

    if isinstance(ultimo, str):
        try:
            ultimo = date.fromisoformat(ultimo)
        except Exception:
            ultimo = None

    streak_atual = usuario.get("streak", 0)

    if ultimo is None or ultimo < hoje:
        if ultimo and (hoje - ultimo).days == 1:
            # Acessou ontem — mantém sequência
            novo_streak = streak_atual + 1
        elif ultimo and ultimo == hoje:
            # Já acessou hoje — não muda
            return streak_atual
        else:
            # Quebrou a sequência
            novo_streak = 1

        supabase.table("users").update({
            "streak": novo_streak,
            "ultimo_acesso": hoje.isoformat()
        }).eq("id", user_id).execute()
        return novo_streak

    return streak_atual


def calcular_vidas_regeneradas(ultima_vida_str: str, vidas_atuais: int) -> int:
    """Regenera 1 vida a cada 30 minutos. Máximo 3."""
    if vidas_atuais >= 3:
        return 3
    try:
        ultima = datetime.fromisoformat(str(ultima_vida_str).replace("Z", "+00:00"))
        agora = datetime.now(timezone.utc)
        minutos = (agora - ultima).total_seconds() / 60
        regeneradas = int(minutos // 30)
        return min(3, vidas_atuais + regeneradas)
    except Exception:
        return vidas_atuais


def atualizar_vidas(user_id: str, vidas: int):
    supabase.table("users").update({
        "vidas": vidas,
        "ultima_vida": datetime.now(timezone.utc).isoformat()
    }).eq("id", user_id).execute()


# ─── AUTH ────────────────────────────────────────────────────────────────────

def registrar_usuario(nome: str, email: str, senha: str):
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": senha,
            "options": {"data": {"nome": nome}}
        })
        if res.user:
            supabase.table("users").upsert({
                "id": res.user.id,
                "email": email,
                "nome": nome,
                "xp": 0,
                "nivel": 1,
                "vidas": 3,
                "streak": 0,
                "badges": []
            }).execute()
            return res.user, None
        return None, "Erro ao criar conta."
    except Exception as e:
        msg = str(e)
        if "already registered" in msg:
            return None, "Este email já está cadastrado."
        return None, msg


def email_existe(email: str) -> bool:
    res = supabase.table("users").select("id").eq("email", email).execute()
    return len(res.data) > 0


def login_usuario(email: str, senha: str):
    if not email_existe(email):
        return None, None, "email_nao_encontrado"
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha
        })
        if res.user and res.session:
            return res.user, res.session, None
        return None, None, "senha_incorreta"
    except Exception:
        return None, None, "senha_incorreta"


def logout_usuario():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass


def buscar_perfil(user_id: str):
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
