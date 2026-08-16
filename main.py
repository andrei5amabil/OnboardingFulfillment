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

class Request(BaseModel):
    first_name: str
    last_name: str
    department: str
    role: str
    start_date: str  # ISO format date string
    employment_type: str
    location: str
    work_location: str
    notes: str = None  # Optional field
    request_id: str 
    hr_manager_id: str
    employee_id: str

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

@app.put("/onboarding/requests")
def create_onboarding_request(item: Request):
    try:
        response = supabase.table("onboarding_requests").insert(item).execute()
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.data)
        return {"status": "success", "message": "Onboarding request created.", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))