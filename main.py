import os
from urllib import response
import uuid
from typing import Literal, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, BackgroundTasks, Body, File, Form, UploadFile
from pydantic import BaseModel, EmailStr, Field, ValidationError
from supabase import create_client, Client
from postgrest import APIError
from datetime import date, datetime, timezone
import json
import ollama
from src.rag.service import build_reasoning_prompt, retrieve_onboarding_policies
import logging
from src.agent.graph import onboarding_flow
from langgraph.types import Command
from src.db import supabase
import traceback
from src.extraction.schemas import DocumentType, ExtractionResponse
from src.extraction.service import DocumentExtractionService
from fastapi.middleware.cors import CORSMiddleware
import time

load_dotenv()
logger = logging.getLogger("uvicorn.error")



app = FastAPI(title="FastAPI + Supabase Setup")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    first_name: str
    last_name: str
    national_id: Optional[str] = None

    department: str
    role: str
    start_date: str  # ISO format date string
    employment_type: str
    location: str
    work_location: str
    manager_id: Optional[str] = None

    shipping_address: Optional[str] = None
    contact_phone: Optional[str] = None

    medical_clearance_status: Optional[bool] = None
    medical_clearance_date: Optional[date] = None

    notes: Optional[str] = ""  # Optional field
    hr_manager_id: str

class DB_Request(BaseModel):
    request_id: str
    created_at: datetime
    employee_id: str
    first_name: str
    last_name: str
    national_id: Optional[str] = None
    department: str
    role: str
    start_date: date
    employment_type: str
    location: str
    work_location: str
    manager_id: Optional[str] = None
    shipping_address: Optional[str] = None
    contact_phone: Optional[str] = None
    medical_clearance_status: Optional[bool] = None
    medical_clearance_date: Optional[date] = None
    hr_manager_id: str
    notes: Optional[str] = None
    status: str
    workflow_runs: Optional[list[dict]] = []

class ReviewPayload(BaseModel):
    action: Literal["approve", "regenerate"]
    note: Optional[str] = ""
    reviewed_by: Optional[str] = "IT_ADMIN"
    approved_discretionary_ids: list[str] = Field(default_factory=list)

class KPIResponse(BaseModel):
    total_onboarded: int
    avg_tokens_per_employee: float
    token_usage_breakdown: dict
    avg_agent_execution_seconds: float
    avg_total_lead_time_seconds: float
    first_pass_approval_rate: float
    escalation_rate: float
    recent_runs: list[dict]

def kickoff_agent_workflow(request_id: str, *args, **kwargs):
    """Initializes and runs the graph until the approval gate interrupt."""
    t0 = time.perf_counter()
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
        "tokens_prompt": 0,
        "tokens_completion": 0,
        "tokens_total": 0,
    }
    try:
        final_state = onboarding_flow.invoke(initial_state, config=config)
        elapsed_sec = round(time.perf_counter() - t0, 2)
        
        prompt_tokens = final_state.get("tokens_prompt", 0)
        completion_tokens = final_state.get("tokens_completion", 0)
        
        supabase.table("workflow_runs").update({
            "execution_time_seconds": elapsed_sec,
            "tokens_prompt": prompt_tokens,
            "tokens_completion": completion_tokens,
            "tokens_total": prompt_tokens + completion_tokens,
            "attempt_number": final_state.get("attempt_count", 1)
        }).eq("request_id", request_id).execute()
        logger.info("⏸️ [Agent Workflow] Paused at approval gate for %s", request_id)
    except Exception as e:
        logger.error("❌ [Agent Workflow] Crashed for %s: %s", request_id, str(e))
        logger.error(traceback.format_exc())
        supabase.table("onboarding_requests").update(
            {"status": "failed"}
        ).eq("request_id", request_id).execute()

def generate_employee_id() -> str:
    try:
        req = supabase.table("employees").select("employee_id").order("created_at", desc=True).limit(1).execute()
        if req.data and len(req.data) > 0 and req.data[0].get("employee_id"):
            last_id = req.data[0]["employee_id"]
            last_num_emp = int(last_id.split("-")[1])
        
        new_id_num = last_num_emp + 1
        return f"EMP-{new_id_num:08d}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating employee ID: {str(e)}")

def verify_request_exists(request_id: str) -> bool:
    """Helper function to check if a request exists in the database."""
    res = supabase.table("onboarding_requests").select("*").eq("request_id", request_id).execute()
    if res.data and len(res.data) > 0:
        return True
    return False

def employee_exists(first_name: str, last_name: str) -> tuple[bool, str]:
    """Helper function to check if an employee already exists in the database."""
    res = supabase.table("onboarding_requests").select("*").eq("first_name", first_name).eq("last_name", last_name).execute()
    if res.data and len(res.data) > 0:
        return (True, "onboarding_requests")
    res = supabase.table("employees").select("*").eq("first_name", first_name).eq("last_name", last_name).execute()
    if res.data and len(res.data) > 0:
        return (True, "employees")
    return (False, "")

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

@app.post(
    "/onboarding/extract-document",
    response_model=ExtractionResponse,
    status_code=status.HTTP_200_OK,
)
def extract_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(...),
):
    """Processes an uploaded document (PDF or Image) through Track A + Track B and returns arbitrated data."""
    try:
        file_bytes = file.file.read()
        result = DocumentExtractionService.process_document(
            file_bytes=file_bytes,
            filename=file.filename or "uploaded_document",
            doc_type=document_type,
            content_type=file.content_type,
        )
        return result
    except ValueError as ve:
        logger.error(f"❌ Document extraction ValueError for {file.filename}: {ve}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        )

@app.post("/onboarding/requests", status_code=status.HTTP_200_OK)
def create_onboarding_request(item: Request, background_tasks: BackgroundTasks):
    try:
        employee_id = generate_employee_id()
        while True:
            request_id = f"ONB-{uuid.uuid4().hex[:8].upper()}"
            if not verify_request_exists(request_id):
                break

        is_employee, table_name = employee_exists(item.first_name, item.last_name)
        if is_employee:
            if table_name == "onboarding_requests":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"An onboarding request for {item.first_name} {item.last_name} already exists.",
                )
            elif table_name == "employees":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"An employee record for {item.first_name} {item.last_name} already exists. If this is intentional, add a digit to the name to differentiate (e.g., John Doe 2).",
                )   
        db_item = {
            "request_id": request_id,
            "employee_id": employee_id,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "department": item.department,
            "national_id": item.national_id,
            "manager_id": item.manager_id,
            "shipping_address": item.shipping_address,
            "contact_phone": item.contact_phone,
            "medical_clearance_status": item.medical_clearance_status,
            "medical_clearance_date": str(item.medical_clearance_date) if item.medical_clearance_date else None,
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
    t0 = time.perf_counter()
    now_iso = datetime.now(timezone.utc).isoformat()
    reviewer = payload.reviewed_by or "IT_ADMIN"

    config = {"configurable": {"thread_id": request_id}}
    state_snapshot = onboarding_flow.get_state(config)

    resume_data = {
        "action": payload.action,
        "note": payload.note or "",
        "reviewed_by": reviewer,
        "approved_discretionary_ids": payload.approved_discretionary_ids,
    }

    try:
        supabase.table("workflow_runs").update({
            "review_action": payload.action,
            "reviewed_by": reviewer,
            "reviewed_at": now_iso,
        }).eq("request_id", request_id).execute()

        if not state_snapshot.tasks:
            req_res = supabase.table("onboarding_requests").select("*").eq("request_id", request_id).single().execute()
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

            catalog_res = (
                supabase.table("software_products")
                .select("name, vendor, license_type, requires_approval, product_id")
                .execute()
            )
            software_catalog = catalog_res.data or []

            reconstructed_state = {
                "request_id": request_id,
                "employee_id": req_res.data["employee_id"],
                "candidate_data": req_res.data,
                "sql_rules": run_data.get("suggested_licenses", []),
                "suggested_licenses": run_data.get("suggested_licenses", []),
                "discretionary_licenses": run_data.get("discretionary_licenses", []),
                "software_catalog": software_catalog,
                "approved_discretionary_ids": payload.approved_discretionary_ids,
                "suggested_hardware": run_data.get("suggested_hardware", {}),
                "policy_tags": run_data.get("policy_citations", [{}])[0].get("tags", []) if run_data.get("policy_citations") else [],
                "flagged_exceptions": run_data.get("policy_citations", [{}])[0].get("flagged_exceptions", []) if run_data.get("policy_citations") else [],
                "citations": [],
                "attempt_count": 1,
                "it_feedback": [payload.note] if payload.note else [],
                "review_action": payload.action,
                "reviewed_by": payload.reviewed_by or "IT_ADMIN",
                "is_approved": (payload.action == "approve"),
                "status": "approved" if payload.action == "approve" else "revision_requested",
                "tokens_prompt": run_data.get("tokens_prompt", 0),
                "tokens_completion": run_data.get("tokens_completion", 0),
                "tokens_total": run_data.get("tokens_total", 0),
            }
            onboarding_flow.update_state(config, reconstructed_state, as_node="human_approval_gate")
            final_state = onboarding_flow.invoke(None, config=config)
        else:
            final_state = onboarding_flow.invoke(Command(resume=resume_data), config=config)

        if payload.action == "approve":
            req_data = supabase.table("onboarding_requests").select("created_at").eq("request_id", request_id).single().execute().data
            if req_data and req_data.get("created_at"):
                created_dt = datetime.fromisoformat(req_data["created_at"].replace("Z", "+00:00"))
                lead_time_sec = round((datetime.now(timezone.utc) - created_dt).total_seconds(), 2)
            else:
                lead_time_sec = 0.0

            supabase.table("onboarding_requests").update({
                "total_lead_time_seconds": lead_time_sec,
                "finalized_at": now_iso,
            }).eq("request_id", request_id).execute()

        elif payload.action == "regenerate":
            elapsed_sec = round(time.perf_counter() - t0, 2)
            prompt_tokens = final_state.get("tokens_prompt", 0)
            comp_tokens = final_state.get("tokens_completion", 0)

            supabase.table("workflow_runs").update({
                "execution_time_seconds": elapsed_sec,
                "tokens_prompt": prompt_tokens,
                "tokens_completion": comp_tokens,
                "tokens_total": prompt_tokens + comp_tokens,
                "attempt_number": final_state.get("attempt_count", 2),
            }).eq("request_id", request_id).execute()

        return {
            "status": "success",
            "action": payload.action,
            "workflow_status": final_state.get("status"),
        }
    except Exception as e:
        logger.error("Review processing failed for %s: %s", request_id, e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/kpis", response_model=KPIResponse)
def get_onboarding_kpis():
    try:
        # Fetch requests with runs
        reqs = supabase.table("onboarding_requests").select("*, workflow_runs(*)").execute().data or []
        runs = supabase.table("workflow_runs").select("*").execute().data or []
        
        total_runs = len(runs)
        completed_reqs = [r for r in reqs if r.get("status") == "completed"]
        
        # 1. Token Metrics
        total_tokens = sum(r.get("tokens_total", 0) for r in runs)
        avg_tokens = round(total_tokens / len(reqs), 1) if reqs else 0.0
        prompt_tokens = sum(r.get("tokens_prompt", 0) for r in runs)
        comp_tokens = sum(r.get("tokens_completion", 0) for r in runs)

        # 2. Execution Time Metrics
        durations = [float(r.get("execution_time_seconds", 0)) for r in runs if r.get("execution_time_seconds")]
        avg_agent_sec = round(sum(durations) / len(durations), 2) if durations else 0.0
        
        lead_times = [float(r.get("total_lead_time_seconds", 0)) for r in completed_reqs if r.get("total_lead_time_seconds")]
        avg_lead_sec = round(sum(lead_times) / len(lead_times), 2) if lead_times else 0.0

        # 3. HITL Pass Rate
        first_pass_approved = sum(
            1 for r in runs 
            if r.get("review_action") == "approve" and r.get("attempt_number") == 1
        )
        total_first_reviews = sum(
            1 for r in runs 
            if r.get("review_action") in ["approve", "regenerate"] and r.get("attempt_number") == 1
        )
        first_pass_rate = round((first_pass_approved / total_first_reviews) * 100, 1) if total_first_reviews else 100.0
        
        manual_interventions = sum(1 for r in reqs if r.get("status") == "requires_manual_intervention")
        escalation_rate = round((manual_interventions / len(reqs)) * 100, 1) if reqs else 0.0

        return {
            "total_onboarded": len(completed_reqs),
            "avg_tokens_per_employee": avg_tokens,
            "token_usage_breakdown": {
                "prompt": prompt_tokens,
                "completion": comp_tokens,
                "total": total_tokens
            },
            "avg_agent_execution_seconds": avg_agent_sec,
            "avg_total_lead_time_seconds": avg_lead_sec,
            "first_pass_approval_rate": first_pass_rate,
            "escalation_rate": escalation_rate,
            "recent_runs": runs[-15:],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))