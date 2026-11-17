import logging
import os
import uuid
from datetime import datetime
from typing import Any, Optional
import json

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

from src.agent.state import OnboardingState
from src.db.client import supabase
from src.integrations.jira.client import jira_client, JiraError
from src.integrations.jira.format import (
    build_logistics_subtask_description,
    build_onboarding_ticket_description,
    build_ticket_summary,
)
from src.integrations.jira.workflow import (
    STATUS_DONE,
    STATUS_IN_PROGRESS,
    STATUS_NEEDS_REVISION,
    STATUS_PENDING_APPROVAL,
)
from src.rag.service import build_reasoning_prompt, retrieve_onboarding_policies
from langgraph.types import interrupt
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from ai_observability import span

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

logger = logging.getLogger("uvicorn.error")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "granite4.2:3b")

DEFAULT_NEW_HIRE_PASSWORD = "Welcome2026!"

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


# --- Jira Ticketing Helpers ---

def _get_jira_ticket(request_id: str, state: OnboardingState) -> tuple[Optional[str], Optional[str]]:
    """Resolve the parent ticket from graph state, falling back to the database."""
    ticket_id = state.get("jira_ticket_id")
    if ticket_id:
        return ticket_id, state.get("jira_ticket_url")
    if not request_id:
        return None, None

    try:
        res = (
            supabase.table("onboarding_requests")
            .select("*")
            .eq("request_id", request_id)
            .single()
            .execute()
        )
        row = res.data or {}
        return row.get("jira_ticket_id"), row.get("jira_ticket_url")
    except Exception as exc:
        logger.warning("Could not load Jira ticket for %s: %s", request_id, exc)
        return None, None


def _persist_jira_ticket(request_id: str, ticket_id: str, ticket_url: Optional[str]) -> None:
    try:
        supabase.table("onboarding_requests").update(
            {"jira_ticket_id": ticket_id, "jira_ticket_url": ticket_url}
        ).eq("request_id", request_id).execute()
    except Exception as exc:
        logger.error(
            "Could not persist Jira ticket %s on request %s (did you apply the Jira migration?): %s",
            ticket_id,
            request_id,
            exc,
        )


def _persist_jira_subtask(request_id: str, subtask_id: str) -> None:
    try:
        supabase.table("onboarding_requests").update(
            {"jira_subtask_id": subtask_id}
        ).eq("request_id", request_id).execute()
    except Exception as exc:
        logger.error(
            "Could not persist Jira sub-task %s on request %s (did you apply the Jira migration?): %s",
            subtask_id,
            request_id,
            exc,
        )


def _ensure_jira_status(ticket_id: Optional[str], status: str) -> None:
    if not ticket_id or not jira_client.is_configured:
        return
    try:
        if not jira_client.ensure_status(ticket_id, status):
            logger.warning("Jira ticket %s could not be moved to '%s'.", ticket_id, status)
    except Exception as exc:
        logger.warning("Jira status sync failed for %s: %s", ticket_id, exc)


def _sync_plan_ticket(
    state: OnboardingState,
    request_id: str,
    attempt_count: int,
) -> dict[str, Any]:
    """Create the parent ticket on the first attempt, otherwise refresh it."""
    if not jira_client.is_configured:
        logger.debug("Jira is not configured; skipping ticket sync for %s.", request_id)
        return {}

    ticket_id, ticket_url = _get_jira_ticket(request_id, state)
    description_state = {
        **state,
        "status": "pending_approval",
        "attempt_count": attempt_count,
    }
    summary = build_ticket_summary(description_state)
    description = build_onboarding_ticket_description(description_state)
    candidate = state.get("candidate_data") or {}
    department = str(candidate.get("department") or "").strip()
    labels = ["onboarding"] + ([f"dept-{department}"] if department else [])

    try:
        if ticket_id:
            jira_client.update_issue(
                ticket_id,
                summary=summary,
                description=description,
                labels=labels,
            )
            # Regenerations update the same ticket and put it back into review.
            _ensure_jira_status(ticket_id, STATUS_PENDING_APPROVAL)
            logger.info("Updated Jira ticket %s for %s (attempt %s).", ticket_id, request_id, attempt_count)
        else:
            issue = jira_client.create_issue(
                summary=summary,
                description=description,
                labels=labels,
            )
            ticket_id = issue.get("key") or ""
            if not ticket_id:
                raise JiraError(f"Jira create response did not include an issue key: {issue}")
            ticket_url = jira_client.browse_url(ticket_id)
            _ensure_jira_status(ticket_id, STATUS_PENDING_APPROVAL)
            logger.info("Created Jira ticket %s for %s.", ticket_id, request_id)
    except Exception as exc:
        logger.error("Jira ticket sync failed for %s: %s", request_id, exc, exc_info=True)
        return {}

    if not ticket_id:
        return {}

    _persist_jira_ticket(request_id, ticket_id, ticket_url)
    return {"jira_ticket_id": ticket_id, "jira_ticket_url": ticket_url}


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
    with span(name="retrieve_onboarding_policies", context={"department": state["candidate_data"].get("department")}):
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

    prompt_tokens = 0
    completion_tokens = 0

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.1,
        num_ctx=4096,
    )
    structured_llm = llm.with_structured_output(OnboardingPlanOutput, include_raw=True)

    try:
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        validated_plan: OnboardingPlanOutput = response["parsed"]

        if not validated_plan:
            raise ValueError("Structured model output returned None.")

        raw_msg = response.get("raw")
        if raw_msg and getattr(raw_msg, "usage_metadata", None):
            prompt_tokens += raw_msg.usage_metadata.get("input_tokens", 0)
            completion_tokens += raw_msg.usage_metadata.get("output_tokens", 0)
        elif raw_msg and getattr(raw_msg, "response_metadata", None):
            prompt_tokens += raw_msg.response_metadata.get("prompt_eval_count", 0)
            completion_tokens += raw_msg.response_metadata.get("eval_count", 0)

    except Exception as e:
        logger.error("Structured hardware planning inference failed: %s", e)
        raise e

    ai_plan = validated_plan.model_dump()
    hardware_plan = ai_plan.get("hardware_provisioning") or {}
    work_loc = str(state.get("candidate_data", {}).get("work_location") or "").strip().lower()
    if work_loc in ("remote", "hybrid"):
        hardware_plan["shipping_required"] = True
    ai_plan["hardware_provisioning"] = hardware_plan

    current_prompt = state.get("tokens_prompt", 0) + prompt_tokens
    current_completion = state.get("tokens_completion", 0) + completion_tokens

    # Keep deterministic compliance flags (computed in fetch_context_node) when
    # merging the LLM's own policy exceptions.
    merged_flags = list(dict.fromkeys(
        list(state.get("flagged_exceptions", [])) + list(ai_plan.get("flagged_exceptions", []))
    ))

    return {
        "suggested_hardware": ai_plan.get("hardware_provisioning", {}),
        "flagged_exceptions": merged_flags,
        "policy_tags": ai_plan.get("policy_citations", []),
        "tokens_prompt": current_prompt,
        "tokens_completion": current_completion,
        "tokens_total": current_prompt + current_completion,
    }

def persist_plan_node(state: OnboardingState) -> dict[str, Any]:
    """Persists workflow run artifacts and places the request into approval state."""
    request_id = state["request_id"]
    attempt_count = state.get("attempt_count", 1)

    # Insert plan record and capture the generated run_id
    insert_res = supabase.table("workflow_runs").insert(
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
            "tokens_prompt": state.get("tokens_prompt", 0),
            "tokens_completion": state.get("tokens_completion", 0),
            "tokens_total": state.get("tokens_total", 0),
            "attempt_number": attempt_count,
        }
    ).execute()

    run_id = insert_res.data[0]["run_id"] if insert_res.data else None

    supabase.table("onboarding_requests").update(
        {"status": "pending_approval"}
    ).eq("request_id", request_id).execute()

    jira_state = _sync_plan_ticket(state, request_id, attempt_count)

    return {
        "status": "pending_approval",
        "current_run_id": run_id,
        **jira_state,
    }

def discretionary_licensing_node(state: OnboardingState) -> dict[str, Any]:
    """Analyzes candidate notes against available catalog in isolation."""
    cand = state.get("candidate_data", {})
    notes = (cand.get("notes") or "").strip()
    feedback = state.get("it_feedback", [])
    catalog = state.get("software_catalog", [])
    sql_rules = state.get("sql_rules", [])

    prompt_tokens = 0
    completion_tokens = 0

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
        llm = ChatOllama(
            model=OLLAMA_MODEL,
            temperature=0.0,
            num_ctx=2048,
        )
        structured_llm = llm.with_structured_output(DiscretionaryListOutput, include_raw=True)
        response = structured_llm.invoke([HumanMessage(content=prompt)])

        parsed: DiscretionaryListOutput = response["parsed"]
        if not parsed:
            raise ValueError("Parsed output returned None.")

        raw_msg = response.get("raw")
        if raw_msg and getattr(raw_msg, "usage_metadata", None):
            prompt_tokens += raw_msg.usage_metadata.get("input_tokens", 0)
            completion_tokens += raw_msg.usage_metadata.get("output_tokens", 0)
        elif raw_msg and getattr(raw_msg, "response_metadata", None):
            prompt_tokens += raw_msg.response_metadata.get("prompt_eval_count", 0)
            completion_tokens += raw_msg.response_metadata.get("eval_count", 0)

        print(f"\n🤖 [DEBUG] PARSED DISCRETIONARY RESPONSE:\n{parsed.model_dump_json(indent=2)}\n")

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

    current_prompt = state.get("tokens_prompt", 0) + prompt_tokens
    current_completion = state.get("tokens_completion", 0) + completion_tokens

    return {
        "discretionary_licenses": valid_proposals,
        "tokens_prompt": current_prompt,
        "tokens_completion": current_completion,
        "tokens_total": current_prompt + current_completion,
    }

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

    #supabase.table("employees").insert(employee_record).execute()
    return {"status": "employee_provisioned"}

def execute_provisioning_node(state: OnboardingState) -> dict[str, Any]:
    cand = state.get("candidate_data", {})
    req_id = state["request_id"]
    emp_id = state["employee_id"]
    if not cand:
        res = supabase.table("onboarding_requests").select("*").eq("request_id", req_id).single().execute()
        cand = res.data or {}
    licenses = state.get("suggested_licenses", [])
    approved_disc_ids = set(state.get("approved_discretionary_ids", []))
    product_ids_to_assign = set()
    for rule in licenses:
        prod = rule.get("software_products") or {}
        pid = prod.get("product_id")
        if pid:
            product_ids_to_assign.add(pid)
    product_ids_to_assign.update(approved_disc_ids)

    ticket_id, _ = _get_jira_ticket(req_id, state)
    _ensure_jira_status(ticket_id, STATUS_IN_PROGRESS)

    rpc_payload = {
        "p_request_id": req_id,
        "p_employee_id": emp_id,
        "p_first_name": cand.get("first_name", ""),
        "p_last_name": cand.get("last_name", ""),
        "p_department": cand.get("department", ""),
        "p_role": cand.get("role", ""),
        "p_start_date": cand.get("start_date"),
        "p_employment_type": cand.get("employment_type", "full-time"),
        "p_location": cand.get("location", ""),
        "p_work_location": cand.get("work_location", "on-site"),
        "p_manager_id": cand.get("manager_id"),
        "p_national_id": cand.get("national_id"),
        "p_shipping_address": cand.get("shipping_address"),
        "p_contact_phone": cand.get("contact_phone"),
        "p_medical_clearance_status": cand.get("medical_clearance_status", False),
        "p_product_ids": list(product_ids_to_assign),
    }

    try:
        rpc_res = supabase.rpc("provision_employee_with_licenses", rpc_payload).execute()
        result = rpc_res.data or {}
        work_email = result.get("work_email")

        if not work_email:
            raise ValueError("RPC completed but did not return a valid work_email.")

        try:
            auth_user = supabase.auth.admin.create_user({
                "email": work_email,
                "password": DEFAULT_NEW_HIRE_PASSWORD,
                "email_confirm": True,
            })
            auth_user_id = auth_user.user.id
        except Exception as auth_err:
            err_lower = str(auth_err).lower()
            if "already" in err_lower and ("registered" in err_lower or "exists" in err_lower):
                existing_users = supabase.auth.admin.list_users()
                auth_user_id = next((u.id for u in existing_users if u.email == work_email), None)
            else:
                logger.error("❌ Failed to create auth.users entry for %s: %s", work_email, auth_err)
                auth_user_id = None

        if auth_user_id:
            supabase.table("users").upsert({
                "user_id": auth_user_id,
                "email": work_email,
                "employee_id": emp_id,
                "role": "new_hire",
                "is_active": True,
            }, on_conflict="user_id").execute()
            logger.info("🔑 [New Hire Provisioned] Created portal account: %s (Pass: %s)", work_email, DEFAULT_NEW_HIRE_PASSWORD)

        # Physical hardware cannot be shipped by the provisioning RPC. Spawn a
        # linked Facilities/Logistics sub-task for the Jira parent ticket.
        hardware = state.get("suggested_hardware") or {}
        if hardware.get("shipping_required") and ticket_id and jira_client.is_configured:
            candidate_name = " ".join(
                part for part in (
                    str(cand.get("first_name") or "").strip(),
                    str(cand.get("last_name") or "").strip(),
                ) if part
            ) or emp_id
            try:
                subtask = jira_client.create_subtask(
                    parent_key=ticket_id,
                    summary=f"[Logistics] Ship hardware to {candidate_name} ({req_id})",
                    description=build_logistics_subtask_description(
                        {**state, "candidate_data": cand}
                    ),
                    labels=["onboarding", "logistics"],
                    assignee_account_id=(
                        jira_client.config.logistics_assignee_account_id or None
                    ),
                )
                subtask_key = subtask.get("key")
                logger.info(
                    "📦 [Jira] Created logistics sub-task %s under %s.",
                    subtask_key,
                    ticket_id,
                )
                if subtask_key:
                    _persist_jira_subtask(req_id, subtask_key)
                    try:
                        jira_client.add_comment(
                            ticket_id,
                            f"Logistics sub-task {subtask_key} created for hardware shipment.",
                        )
                    except Exception as comment_exc:
                        logger.warning("Could not comment on Jira ticket %s: %s", ticket_id, comment_exc)
            except Exception as jira_exc:
                logger.error(
                    "Could not create Jira logistics sub-task for %s: %s",
                    req_id,
                    jira_exc,
                )

        return {
            "status": "provisioned",
            "work_email": work_email,
            "provisioning_error": None,
        }

    except Exception as exc:
        err_msg = str(exc)
        logger.error(f"❌ [Provisioning Engine] Atomic transaction rolled back: {err_msg}")
        return {
            "status": "provisioning_failed",
            "provisioning_error": err_msg,
        }

def finalize_workflow_node(state: OnboardingState) -> dict[str, Any]:
    request_id = state.get("request_id")
    reviewer = state.get("reviewed_by") or "IT_ADMIN"
    ticket_id, _ = _get_jira_ticket(request_id, state)

    if state.get("status") == "provisioning_failed":
        if request_id:
            supabase.table("onboarding_requests").update(
                {"status": "provisioning_failed"}
            ).eq("request_id", request_id).execute()

        if ticket_id and jira_client.is_configured:
            try:
                jira_client.add_comment(
                    ticket_id,
                    "Provisioning failed and was rolled back: "
                    f"{state.get('provisioning_error') or 'unknown error'}",
                )
            except Exception as exc:
                logger.warning("Could not comment on Jira ticket %s: %s", ticket_id, exc)
        return {"status": "failed"}

    supabase.table("onboarding_requests").update(
        {"status": "completed"}
    ).eq("request_id", request_id).execute()

    supabase.table("workflow_runs").update(
        {
            "reviewed_by": reviewer,
            "updated_at": datetime.now().isoformat(),
        }
    ).eq("request_id", request_id).execute()

    if ticket_id:
        _ensure_jira_status(ticket_id, STATUS_DONE)
        if jira_client.is_configured:
            try:
                work_email = state.get("work_email")
                message = "Provisioning completed by the Onboarding Portal."
                if work_email:
                    message += f" Work email: {work_email}"
                jira_client.add_comment(ticket_id, message)
            except Exception as exc:
                logger.warning("Could not comment on Jira ticket %s: %s", ticket_id, exc)

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

    ticket_id, _ = _get_jira_ticket(request_id, state)
    if ticket_id and jira_client.is_configured:
        try:
            jira_client.add_comment(
                ticket_id,
                "Escalated: the maximum number of revision attempts was reached. "
                "Manual IT intervention is required.",
            )
        except Exception as exc:
            logger.warning("Could not comment on Jira ticket %s: %s", ticket_id, exc)

    return {"status": "requires_manual_intervention"}