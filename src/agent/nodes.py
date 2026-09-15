import logging
import os
import uuid
from datetime import datetime
from typing import Any, Optional

from dotenv import load_dotenv
import ollama
from pydantic import BaseModel, Field, ValidationError

from src.agent.state import OnboardingState
from src.db.client import supabase
from src.rag.service import build_reasoning_prompt, retrieve_onboarding_policies
from langgraph.types import interrupt
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

logger = logging.getLogger("uvicorn.error")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "granite4.2:3b")

# --- Pydantic Output Schemas ---

class HardwarePlan(BaseModel):
    laptop: Optional[str] = None
    peripherals: list[str] = Field(default_factory=list)
    shipping_required: bool = False


class OnboardingPlanOutput(BaseModel):
    hardware_provisioning: HardwarePlan
    flagged_exceptions: list[str] = Field(default_factory=list)
    policy_citations: list[str] = Field(default_factory=list)


# --- Helper Functions ---

def deduplicate_rules(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Prioritizes role-specific rules over department and global defaults."""
    def rule_priority(r: dict[str, Any]) -> int:
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


# --- Agentic Planning Nodes ---

def fetch_context_node(state: OnboardingState) -> dict[str, Any]:
    """Fetches candidate profile data and deterministic SQL assignment rules."""
    request_id = state["request_id"]

    # Update database status to processing
    supabase.table("onboarding_requests").update(
        {"status": "processing_rules"}
    ).eq("request_id", request_id).execute()

    # Retrieve candidate record
    req_res = (
        supabase.table("onboarding_requests")
        .select("*")
        .eq("request_id", request_id)
        .single()
        .execute()
    )
    if not req_res.data:
        raise ValueError(f"Onboarding request {request_id} not found")
    
    candidate_data = req_res.data
    department = candidate_data.get("department", "")
    role = candidate_data.get("role", "")

    # Query deterministic software assignment rules
    filter_query = (
        f"department.is.null,"
        f'and(department.eq."{department}",role.is.null),'
        f'and(department.eq."{department}",role.eq."{role}")'
    )

    rules_res = (
        supabase.table("product_assignment_rules")
        .select(
            "rule_id, access_level, is_mandatory, requires_approval, "
            "software_products(product_id, name, vendor, license_type)"
        )
        .or_(filter_query)
        .execute()
    )
    deduped_licenses = deduplicate_rules(rules_res.data or [])

    return {
        "candidate_data": candidate_data,
        "employee_id": candidate_data["employee_id"],
        "sql_rules": deduped_licenses,
        "suggested_licenses": deduped_licenses,
        "status": "processing_rules",
    }


def policy_rag_node(state: OnboardingState) -> dict[str, Any]:
    """Retrieves corporate compliance policies matching the hire context."""
    citations = retrieve_onboarding_policies(state["candidate_data"])
    return {"citations": citations}


def llm_planning_node(state: OnboardingState) -> dict[str, Any]:
    """Generates the hardware/policy plan, incorporating prior IT revision feedback if retrying."""
    feedback = state.get("it_feedback", [])
    
    prompt = build_reasoning_prompt(
        state["candidate_data"],
        state["sql_rules"],
        state["citations"],
    )

    # Append revision context from previous rejection attempts
    if feedback:
        formatted_feedback = "\n".join(f"- Attempt #{i+1} IT Feedback: {note}" for i, note in enumerate(feedback))
        prompt += f"\n\n### IT REVIEWER REVISION REQUESTS\n{formatted_feedback}\nAdjust the output strictly to satisfy this feedback."

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
        format=OnboardingPlanOutput.model_json_schema(),
        options={"temperature": 0.1},
    )

    try:
        validated_plan = OnboardingPlanOutput.model_validate_json(
            response["message"]["content"]
        )
    except ValidationError as ve:
        logger.error("LLM JSON schema mismatch: %s", ve.json())
        raise ve

    ai_plan = validated_plan.model_dump()
    return {
        "suggested_hardware": ai_plan.get("hardware_provisioning", {}),
        "flagged_exceptions": ai_plan.get("flagged_exceptions", []),
        "policy_tags": ai_plan.get("policy_citations", []),
    }

def persist_plan_node(state: OnboardingState) -> dict[str, Any]:
    """Persists workflow run artifacts and places the request into approval state."""
    request_id = state["request_id"]

    # Clear stale runs
    supabase.table("workflow_runs").delete().eq("request_id", request_id).execute()

    # Commit generated plan
    supabase.table("workflow_runs").insert(
        {
            "request_id": request_id,
            "suggested_licenses": state["suggested_licenses"],
            "suggested_hardware": state["suggested_hardware"],
            "policy_citations": [
                {
                    "tags": state["policy_tags"],
                    "raw_citations": [
                        {
                            "code": c["policy_code"],
                            "section": c["section_title"],
                        }
                        for c in state["citations"]
                    ],
                    "flagged_exceptions": state["flagged_exceptions"],
                }
            ],
        }
    ).execute()

    supabase.table("onboarding_requests").update(
        {"status": "pending_approval"}
    ).eq("request_id", request_id).execute()

    return {"status": "pending_approval"}


# --- Deterministic DB Execution Nodes ---

def provision_employee_node(state: OnboardingState) -> dict[str, Any]:
    """Inserts a finalized employee profile into the employees table."""
    cand = state["candidate_data"]
    emp_id = state["employee_id"]

    # Fallback to refetch if state lacks candidate data on graph resume
    if not cand:
        res = (
            supabase.table("onboarding_requests")
            .select("*")
            .eq("request_id", state["request_id"])
            .single()
            .execute()
        )
        cand = res.data or {}

    clean_first = cand.get("first_name", "").strip().lower()
    clean_last = cand.get("last_name", "").strip().lower()
    work_email = f"{clean_first}.{clean_last}@atossoftware.com"

    employee_record = {
        "employee_id": emp_id,
        "onboarding_request_id": state["request_id"],
        "first_name": cand["first_name"],
        "last_name": cand["last_name"],
        "work_email": work_email,
        "department": cand["department"],
        "role": cand["role"],
        "start_date": cand["start_date"],
        "employment_type": cand["employment_type"],
        "location": cand["location"],
        "work_location": cand["work_location"],
        "manager_id": cand.get("manager_id"),
        "status": "active",
        "updated_at": datetime.now().isoformat(),
    }

    supabase.table("employees").insert(employee_record).execute()
    return {"status": "employee_provisioned"}


def assign_licenses_node(state: OnboardingState) -> dict[str, Any]:
    emp_id = state.get("employee_id")
    req_id = state.get("request_id")
    licenses = state.get("suggested_licenses", [])
    
    # Refetch fallback if licenses missing
    if not licenses and req_id:
        run_res = (
            supabase.table("workflow_runs")
            .select("suggested_licenses")
            .eq("request_id", req_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if run_res.data:
            licenses = run_res.data[0].get("suggested_licenses", [])

    records = []
    for rule in licenses:
        prod = rule.get("software_products") or {}
        prod_id = prod.get("product_id")
        if not prod_id:
            continue

        records.append(
            {
                "assignment_id": f"LIC-{uuid.uuid4().hex[:8].upper()}",
                "employee_id": emp_id,
                "product_id": prod_id,
                "status": "active",
                "assigned_at": datetime.now().isoformat(),
            }
        )

    if records:
        supabase.table("license_assignments").insert(records).execute()

    return {"status": "licenses_assigned"}

def finalize_workflow_node(state: OnboardingState) -> dict[str, Any]:
    request_id = state.get("request_id")
    reviewer = state.get("reviewed_by") or "IT_ADMIN"

    supabase.table("onboarding_requests").update(
        {"status": "completed"}
    ).eq("request_id", request_id).execute()

    supabase.table("workflow_runs").update(
        {
            "reviewed_by": reviewer,
            "updated_at": datetime.now().isoformat(),
        }
    ).eq("request_id", request_id).execute()

    return {"status": "completed"}

def human_approval_gate_node(state: OnboardingState) -> dict[str, Any]:
    """Yields current plan to the UI and pauses execution until an IT decision is submitted."""
    review_input = interrupt(
        {
            "request_id": state["request_id"],
            "attempt_count": state.get("attempt_count", 1),
            "suggested_licenses": state.get("suggested_licenses", []),
            "suggested_hardware": state.get("suggested_hardware", {}),
            "flagged_exceptions": state.get("flagged_exceptions", []),
            "it_feedback": state.get("it_feedback", []),
        }
    )

    action = review_input.get("action")  # "approve" or "regenerate"
    note = review_input.get("note", "").strip()
    reviewer = review_input.get("reviewed_by", "IT_ADMIN")

    feedback_list = list(state.get("it_feedback", []))
    if note:
        feedback_list.append(note)

    if action == "approve":
        return {
            "is_approved": True,
            "review_action": "approve",
            "reviewed_by": reviewer,
            "it_feedback": feedback_list,
            "status": "approved",
        }

    return {
        "is_approved": False,
        "review_action": "regenerate",
        "reviewed_by": reviewer,
        "attempt_count": state.get("attempt_count", 1) + 1,
        "it_feedback": feedback_list,
        "status": "revision_requested",
    }


def handle_max_retries_node(state: OnboardingState) -> dict[str, Any]:
    """Escalates requests that exceed allowed regeneration cycles to manual intervention."""
    request_id = state["request_id"]
    supabase.table("onboarding_requests").update(
        {"status": "requires_manual_intervention"}
    ).eq("request_id", request_id).execute()

    return {"status": "requires_manual_intervention"}