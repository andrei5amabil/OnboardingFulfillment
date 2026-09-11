# src/db/client.py
import os
from dotenv import load_dotenv
from supabase import Client, create_client
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file.")

# Shared singleton instance
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)