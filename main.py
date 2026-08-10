import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="FastAPI + Supabase Setup")

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.get("/health/supabase")
def check_sb_connection():
    try:
        response = supabase.table("test").select("*").limit(1).execute()
        return {"status": "success",
                "message": "Connected to Supabase successfully.", 
                "data": response.data
                }
    except Exception as e:
        error_str = str(e)
        
        # If Supabase returns a PostgREST error (like table doesn't exist),
        # it confirms the network request reached your local Supabase instance!
        if "PGRST" in error_str or "relation" in error_str or "42P01" in error_str:
            return {
                "status": "connected",
                "message": "Local Supabase connection verified! (The 'test' table does not exist yet).",
                "raw_response": error_str
            }
        
        # If Docker is stopped or URL is wrong
        raise HTTPException(
            status_code=500,
            detail=f"Could not reach local Supabase instance: {error_str}"
        )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    supabase_response = supabase.table("items").update(item.dict()).eq("id", item_id).execute()
    if supabase_response.status_code != 200:
        raise HTTPException(status_code=supabase_response.status_code, detail=supabase_response.data)
    return {"item_id": item_id, "item": supabase_response.data}