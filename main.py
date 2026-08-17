import os
import uuid
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from postgrest import APIError

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
    notes: Optional[str] = ""  # Optional field
    hr_manager_id: str

def generate_employee_id() -> str:
    try:
        #res = supabase.table("employees").select("employee_id").order("created_at", desc=True).limit(1).execute()
        req = supabase.table("onboarding_requests").select("employee_id").order("created_at", desc=True).limit(1).execute()

        #if (res.data and len(res.data) > 0 and res.data[0].get("employee_id") and 
        if req.data and len(req.data) > 0 and req.data[0].get("employee_id"):
            last_id = req.data[0]["employee_id"]
            last_num = int(last_id.split("-")[1])
            new_id_num = last_num + 1
        else:
            new_id_num = 1
        return f"EMP-{new_id_num:04d}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating employee ID: {str(e)}")

@app.get("/health/supabase")
def check_sb_connection():
    try:
        response = supabase.table("onboarding_requests").select("*").limit(1).execute()
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
                "message": "Local Supabase connection verified! (The 'onboarding_requests' table does not exist yet).",
                "raw_response": error_str
            }
        
        # If Docker is stopped or URL is wrong
        raise HTTPException(
            status_code=500,
            detail=f"Could not reach local Supabase instance: {error_str}"
        )

@app.post("/onboarding/requests", status_code=status.HTTP_200_OK)
def create_onboarding_request(item: Request):
    try:
        employee_id = generate_employee_id()
        request_id = f"ONB-{uuid.uuid4().hex[:8].upper()}"
        db_item = {
            "request_id": request_id,
            "employee_id": employee_id,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "department": item.department,
            "role": item.role,
            "start_date": item.start_date,
            "employment_type": item.employment_type,
            "location": item.location,
            "work_location": item.work_location,
            "notes": item.notes,
            "hr_manager_id": item.hr_manager_id,
            "status": "pending"
        }
        response = supabase.table("onboarding_requests").insert(db_item).execute()

        return {
            "status": "success", 
            "message": "Onboarding request created.", 
            "data": response.data[0]
        }
    except APIError as err:
        # err contains details, message, code, and hint from PostgREST
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": err.message,
                "code": err.code,
                "details": err.details,
                "hint": err.hint,
            },
        )