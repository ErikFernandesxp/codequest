from backend.supabase_client import supabase

def criar_usuario(email):
    return supabase.table("users").insert({"email": email}).execute()

def salvar_progresso(user_id, linguagem, fase):
    return supabase.table("progress").insert({
        "user_id": user_id,
        "linguagem": linguagem,
        "fase": fase,
        "concluido": True
    }).execute()

def buscar_progresso(user_id):
    return supabase.table("progress").select("*").eq("user_id", user_id).execute()