import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL", "")
key = os.getenv("SUPABASE_KEY", "")

if not url or not key:
    raise ValueError("❌ SUPABASE_URL e SUPABASE_KEY precisam estar no arquivo .env")

supabase = create_client(url, key)