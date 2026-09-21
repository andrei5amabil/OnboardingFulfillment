import logging
import os
import uuid
from datetime import datetime
from typing import Any, Optional
import json

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
    laptop: Optional[str] = Field(
        default=None,
        description="Recommended laptop tier/model (e.g., 'MacBook Pro 16\" / Dell XPS 15 (Dev Tier)' or 'ThinkPad T14 (Standard Tier)')",
    )
    peripherals: list[str] = Field(
        default_factory=list,
        description="List of required equipment/peripherals (e.g., 'Dual 27\" Monitors', 'USB-C Dock', 'YubiKey 5C NFC', 'Ergonomic Keyboard')",
    )
    shipping_required: bool = Field(
        default=False,
        description="Set to true if candidate work_location is 'remote' or requires home delivery; false if onsite.",
    )

class DiscretionaryLicenseProposal(BaseModel):
    product_id: str = Field(
        description="The exact product_id from the AVAILABLE SOFTWARE CATALOG (e.g., 'PRD-001')."
    )
    justification: str = Field(
        description="Concise rationale explaining why candidate notes or project tasks require this specific software."
    )

class DiscretionaryListOutput(BaseModel):
    discretionary_licenses: list[DiscretionaryLicenseProposal] = Field(default_factory=list)

class OnboardingPlanOutput(BaseModel):
    hardware_provisioning: HardwarePlan
    flagged_exceptions: list[str] = Field(
        default_factory=list,
        description="Any policy violations, security flags, or non-standard requirements requiring IT intervention.",
    )
    policy_citations: list[str] = Field(
        default_factory=list,
        description="List of policy clause tags or document codes referenced (e.g., ['POL-SEC-01', 'HARDWARE-STD-02']).",
    )


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

    flagged = list(state.get("flagged_exceptions", []))

    if candidate_data.get("medical_clearance_status") is False:
        flagged.append(
            "COMPLIANCE GATE: Candidate marked UNFIT or medical clearance unconfirmed. "
            "Provisioning halted pending occupational health re-examination."
        )

    work_loc = (candidate_data.get("work_location") or "").lower()
    if work_loc in ["remote", "hybrid"] and not candidate_data.get("shipping_address"):
        flagged.append(
            "LOGISTICS WARNING: Remote/Hybrid hire is missing a valid equipment shipping address."
        )

    if not candidate_data.get("national_id"):
        flagged.append("COMPLIANCE NOTICE: National ID / CNP is missing from the record.")

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

    catalog_res = (
        supabase.table("software_products")
        .select("name, vendor, license_type, requires_approval, product_id")
        .execute()
    )
    software_catalog = catalog_res.data or []

    return {
        "candidate_data": candidate_data,
        "employee_id": candidate_data["employee_id"],
        "sql_rules": deduped_licenses,
        "suggested_licenses": deduped_licenses,
        "software_catalog": software_catalog,
        "status": "processing_rules",
        "flagged_exceptions": flagged,
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

    if feedback:
        formatted_feedback = "\n".join(
            f"- Attempt #{i+1} IT Feedback: {note}" for i, note in enumerate(feedback)
        )
        prompt += f"\n\n### IT REVIEWER REVISION REQUESTS (HARDWARE / POLICIES)\n{formatted_feedback}\nAdjust the hardware and shipping configuration strictly to satisfy this feedback."

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            format=OnboardingPlanOutput.model_json_schema(),
            options={"temperature": 0.1, "num_ctx": 4096},
        )
        raw_content = response.get("message", {}).get("content", "").strip()
    except Exception as e:
        logger.warning("Grammar-constrained inference failed (%s). Falling back to generic JSON mode.", e)
        raw_content = ""

    # Fallback to generic JSON if grammar fails or returns empty
    if not raw_content:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}\n\nRespond strictly with a JSON object matching keys: 'hardware_provisioning', 'flagged_exceptions', 'policy_citations'.",
                }
            ],
            format="json",
            options={"temperature": 0.1, "num_ctx": 4096},
        )
        raw_content = response.get("message", {}).get("content", "").strip()

    try:
        validated_plan = OnboardingPlanOutput.model_validate_json(raw_content)
    except ValidationError as ve:
        logger.error("Hardware planning schema validation failed: %s\nRaw output: %s", ve.json(), raw_content)
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
            "discretionary_licenses": state.get("discretionary_licenses", []),
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

def discretionary_licensing_node(state: OnboardingState) -> dict[str, Any]:
    """Analyzes candidate notes against available catalog in isolation."""
    cand = state.get("candidate_data", {})
    notes = (cand.get("notes") or "").strip()
    feedback = state.get("it_feedback", [])
    catalog = state.get("software_catalog", [])
    sql_rules = state.get("sql_rules", [])

    print("\n" + "=" * 50)
    print("🔍 [DEBUG: discretionary_licensing_node] INPUT STATE:")
    print(f"  - Request ID: {state.get('request_id')}")
    print(f"  - Notes: '{notes}'")
    print(f"  - IT Feedback: {feedback}")
    print(f"  - Catalog items loaded: {len(catalog)}")
    print(f"  - SQL Rules (Baseline assigned): {len(sql_rules)}")

    # Safety Fallback: Re-fetch catalog if missing from rehydrated state
    if not catalog:
        print("⚠️ [DEBUG] software_catalog was EMPTY in state! Fetching directly from DB...")
        cat_res = supabase.table("software_products").select("name, vendor, license_type, requires_approval, product_id").execute()
        catalog = cat_res.data or []
        print(f"  - Recovered {len(catalog)} catalog items from Supabase.")

    # Check fast path
    if not notes and not feedback:
        print("🛑 [DEBUG] Fast path exit: Both 'notes' and 'it_feedback' are empty. Returning [].")
        print("=" * 50 + "\n")
        return {"discretionary_licenses": []}

    assigned_ids = {
        (r.get("software_products") or {}).get("product_id")
        for r in sql_rules
        if (r.get("software_products") or {}).get("product_id")
    }

    available_catalog = [p for p in catalog if p.get("product_id") not in assigned_ids]
    print(f"  - Available catalog after deduplication: {len(available_catalog)} items")
    
    if not available_catalog:
        print("🛑 [DEBUG] No available products remaining in catalog! Returning [].")
        print("=" * 50 + "\n")
        return {"discretionary_licenses": []}

    catalog_text = "\n".join([
        f"- ID: {p['product_id']} | Product: {p['name']} | Type: {p.get('license_type', 'Standard')}"
        for p in available_catalog
    ])

    feedback_text = ""
    if feedback:
        feedback_text = f"\n### IT REVIEWER FEEDBACK (SOFTWARE REQUESTS):\n" + "\n".join(feedback)

    prompt = f"""You are the Enterprise Software Licensing Specialist.
Review the candidate's custom notes and IT feedback to identify additional SOFTWARE products required from the catalog.

### CANDIDATE DETAILS
- Role: {cand.get('role')}
- Department: {cand.get('department')}
- Custom Notes: {notes or "None"}
{feedback_text}

### AVAILABLE SOFTWARE CATALOG (Pick ONLY from this list)
{catalog_text}

### INSTRUCTIONS
1. Evaluate whether the Custom Notes or IT Feedback request specific software tools.
2. Match requested tools strictly against the AVAILABLE SOFTWARE CATALOG using the exact 'product_id'.
3. Ignore all hardware, monitors, laptops, or physical gear mentioned in the notes (handled by another team).
4. If no extra software is needed or justified, return an empty array.

Return strictly valid JSON matching the schema."""

    print("\n📝 [DEBUG] PROMPT SENT TO OLLAMA:")
    print("-" * 40)
    print(prompt)
    print("-" * 40)

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            format=DiscretionaryListOutput.model_json_schema(),
            options={"temperature": 0.0, "num_ctx": 2048},
        )
        raw_output = response.get("message", {}).get("content", "").strip()
        print(f"\n🤖 [DEBUG] RAW OLLAMA RESPONSE:\n{raw_output}\n")
        parsed = DiscretionaryListOutput.model_validate_json(raw_output)
    except Exception as e:
        print(f"❌ [DEBUG] Parsing/Ollama invocation failed: {e}")
        print("=" * 50 + "\n")
        return {"discretionary_licenses": []}

    catalog_map = {p["product_id"]: p["name"] for p in available_catalog}
    valid_proposals = []
    
    for item in parsed.discretionary_licenses:
        print(f"  - Model proposed: product_id='{item.product_id}' | reason='{item.justification}'")
        if item.product_id in catalog_map:
            print(f"    ✅ Matched to catalog: '{catalog_map[item.product_id]}'")
            valid_proposals.append({
                "product_id": item.product_id,
                "name": catalog_map[item.product_id],
                "justification": item.justification,
            })
        else:
            print(f"    ❌ REJECTED: product_id '{item.product_id}' not found in available catalog!")

    print(f"\n📦 [DEBUG] FINAL DISCRETIONARY OUTPUT: {valid_proposals}")
    print("=" * 50 + "\n")
    return {"discretionary_licenses": valid_proposals}

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
        "national_id": cand.get("national_id"),
        "work_email": work_email,
        "department": cand["department"],
        "role": cand["role"],
        "start_date": cand["start_date"],
        "employment_type": cand["employment_type"],
        "location": cand["location"],
        "work_location": cand["work_location"],
        "medical_clearance_status": cand["medical_clearance_status"],
        "shipping_address": cand.get("shipping_address"),
        "contact_phone": cand.get("contact_phone"),
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
    approved_disc_ids = set(state.get("approved_discretionary_ids", []))
    
    # Refetch fallback if licenses missing
    if not licenses and req_id:
        run_res = (
            supabase.table("workflow_runs")
            .select("suggested_licenses, discretionary_licenses")
            .eq("request_id", req_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if run_res.data:
            licenses = run_res.data[0].get("suggested_licenses", [])

    product_ids_to_assign = set()

    for rule in licenses:
        prod = rule.get("software_products") or {}
        prod_id = prod.get("product_id")
        if prod_id:
            product_ids_to_assign.add(prod_id)

    for d_id in approved_disc_ids:
        product_ids_to_assign.add(d_id)

    records = [
        {
            "assignment_id": f"LIC-{uuid.uuid4().hex[:8].upper()}",
            "employee_id": emp_id,
            "product_id": pid,
            "status": "active",
            "assigned_at": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        for pid in product_ids_to_assign
    ]

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
            "discretionary_licenses": state.get("discretionary_licenses", []),
            "suggested_hardware": state.get("suggested_hardware", {}),
            "flagged_exceptions": state.get("flagged_exceptions", []),
            "it_feedback": state.get("it_feedback", []),
        }
    )

    action = review_input.get("action")  # "approve" or "regenerate"
    note = review_input.get("note", "").strip()
    reviewer = review_input.get("reviewed_by", "IT_ADMIN")
    approved_disc_ids = review_input.get("approved_discretionary_ids", [])

    feedback_list = list(state.get("it_feedback", []))
    if note:
        feedback_list.append(note)

    if action == "approve":
        return {
            "is_approved": True,
            "review_action": "approve",
            "reviewed_by": reviewer,
            "it_feedback": feedback_list,
            "approved_discretionary_ids": approved_disc_ids,
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