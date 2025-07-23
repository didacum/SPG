import os
from supabase import create_client, Client

def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not (url and key):
      raise RuntimeError("Missing SUPABASE_URL or SERVICE_ROLE_KEY env vars")
    return create_client(url, key)