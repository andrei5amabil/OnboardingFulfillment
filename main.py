import os
from urllib import response
import uuid
from typing import Literal, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, BackgroundTasks, Body
from pydantic import BaseModel, EmailStr, Field, ValidationError
from supabase import create_client, Client
from postgrest import APIError
from datetime import date, datetime
import json
import ollama
from src.rag.service import build_reasoning_prompt, retrieve_onboarding_policies
import logging
from src.agent.graph import onboarding_flow
from langgraph.types import Command
from src.db import supabase
import traceback

load_dotenv()
logger = logging.getLogger("uvicorn.error")



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

class DB_Request(BaseModel):
    request_id: str
    created_at: datetime
    employee_id: str
    first_name: str
    last_name: str
    department: str
    role: str
    start_date: date
    employment_type: str
    location: str
    work_location: str
    hr_manager_id: str
    notes: Optional[str] = None
    status: str
    workflow_runs: Optional[list[dict]] = []

class ReviewPayload(BaseModel):
    action: Literal["approve", "regenerate"]
    note: Optional[str] = ""
    reviewed_by: Optional[str] = "IT_ADMIN"

def kickoff_agent_workflow(request_id: str, *args, **kwargs):
    """Initializes and runs the graph until the approval gate interrupt."""
    logger.info("▶️ [Agent Workflow] Starting generation for %s", request_id)
    config = {"configurable": {"thread_id": request_id}}
    initial_state = {
        "request_id": request_id,
        "employee_id": "",
        "candidate_data": {},
        "sql_rules": [],
        "citations": [],
        "suggested_licenses": [],
        "suggested_hardware": {},
        "policy_tags": [],
        "flagged_exceptions": [],
        "attempt_count": 1,
        "it_feedback": [],
        "review_action": None,
        "reviewed_by": None,
        "is_approved": False,
        "status": "processing_rules",
    }
    try:
        onboarding_flow.invoke(initial_state, config=config)
        logger.info("⏸️ [Agent Workflow] Paused at approval gate for %s", request_id)
    except Exception as e:
        logger.error("❌ [Agent Workflow] Crashed for %s: %s", request_id, str(e))
        logger.error(traceback.format_exc())
        supabase.table("onboarding_requests").update(
            {"status": "failed"}
        ).eq("request_id", request_id).execute()

def deduplicate_rules(rules: list[dict]) -> list[dict]:
    """Ensures role-specific rules take precedence over department or global defaults."""

    def rule_priority(r: dict) -> int:
        if r.get("role"):
            return 3
        if r.get("department"):
            return 2
        return 1

    sorted_rules = sorted(rules, key=rule_priority)
    product_map = {}
    for r in sorted_rules:
        prod = r.get("software_products")
        if prod and "product_id" in prod:
            product_map[prod["product_id"]] = r
    return list(product_map.values())

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
def create_onboarding_request(item: Request, background_tasks: BackgroundTasks):
    try:
        employee_id = generate_employee_id()
        request_id = f"ONB-{uuid.uuid4().hex[:8].upper()}"
        
        # 1. Insert directly in 'processing_rules' so the UI immediately shows active progress
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
            "status": "processing_rules",
        }
        response = supabase.table("onboarding_requests").insert(db_item).execute()
        
        # 2. Queue the single-parameter agent workflow
        background_tasks.add_task(kickoff_agent_workflow, request_id)

        return {
            "status": "success",
            "message": "Onboarding request created and agent initialized.",
            "data": response.data[0],
        }
    except APIError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": err.message,
                "code": err.code,
                "details": err.details,
                "hint": err.hint,
            },
        )

@app.get("/onboarding/requests", response_model=list[DB_Request])
def provide_requests(status: Optional[str] = None, limit: int = 20):
    try:
        query = (
            supabase.table("onboarding_requests")
            .select("*, workflow_runs(*)")
            .order("created_at", desc=True)
            .limit(limit)
        )
        if status:
            query = query.eq("status", status)
        return query.execute().data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/onboarding/requests", status_code=status.HTTP_200_OK)
def create_onboarding_request(item: Request, background_tasks: BackgroundTasks):
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
            "status": "pending_onboarding",
        }
        response = supabase.table("onboarding_requests").insert(db_item).execute()
        
        # Hand full plan generation directly to the agent
        background_tasks.add_task(kickoff_agent_workflow, request_id)

        return {
            "status": "success",
            "message": "Onboarding request created and agent initialized.",
            "data": response.data[0],
        }
    except APIError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": err.message,
                "code": err.code,
                "details": err.details,
                "hint": err.hint,
            },
        )

@app.post("/onboarding/requests/{request_id}/generate-plan")
def trigger_plan_generation(request_id: str, background_tasks: BackgroundTasks):
    """Manual fallback to initiate or retry plan generation."""
    supabase.table("onboarding_requests").update(
        {"status": "processing_rules"}
    ).eq("request_id", request_id).execute()

    background_tasks.add_task(kickoff_agent_workflow, request_id)
    return {"status": "success", "message": f"Plan generation queued for {request_id}"}
    
@app.post("/onboarding/requests/{request_id}/review")
def review_onboarding_plan(request_id: str, payload: ReviewPayload):
    """Resumes the workflow, rehydrating from Supabase if thread state was lost in memory."""
    config = {"configurable": {"thread_id": request_id}}
    state_snapshot = onboarding_flow.get_state(config)

    # If server restarted or request was generated in another process, rehydrate from DB
    if not state_snapshot.tasks:
        req_res = (
            supabase.table("onboarding_requests")
            .select("*")
            .eq("request_id", request_id)
            .single()
            .execute()
        )
        if not req_res.data:
            raise HTTPException(status_code=404, detail="Request not found")

        run_res = (
            supabase.table("workflow_runs")
            .select("*")
            .eq("request_id", request_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        run_data = run_res.data[0] if run_res.data else {}

        reconstructed_state = {
            "request_id": request_id,
            "employee_id": req_res.data["employee_id"],
            "candidate_data": req_res.data,
            "sql_rules": run_data.get("suggested_licenses", []),
            "suggested_licenses": run_data.get("suggested_licenses", []),
            "suggested_hardware": run_data.get("suggested_hardware", {}),
            "policy_tags": [],
            "flagged_exceptions": [],
            "citations": [],
            "attempt_count": 1,
            "it_feedback": [payload.note] if payload.note else [],
            "review_action": payload.action,
            "reviewed_by": payload.reviewed_by or "IT_ADMIN",
            "is_approved": (payload.action == "approve"),
            "status": "approved" if payload.action == "approve" else "revision_requested",
        }

        # Inject state directly as human_approval_gate so the conditional edge routes immediately
        onboarding_flow.update_state(
            config,
            reconstructed_state,
            as_node="human_approval_gate",
        )
        final_state = onboarding_flow.invoke(None, config=config)

    else:
        # Standard in-memory resume
        final_state = onboarding_flow.invoke(
            Command(
                resume={
                    "action": payload.action,
                    "note": payload.note or "",
                    "reviewed_by": payload.reviewed_by or "IT_ADMIN",
                }
            ),
            config=config,
        )

    return {
        "status": "success",
        "action": payload.action,
        "workflow_status": final_state.get("status"),
    }