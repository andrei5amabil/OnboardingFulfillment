import logging
import json
from src.agent.graph import onboarding_flow
from src.db import supabase

# Enable console logging for standalone run
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# 1. Fetch latest candidate request
req = (
    supabase.table("onboarding_requests")
    .select("request_id, status")
    .order("created_at", desc=True)
    .limit(1)
    .execute()
)

if not req.data:
    print("❌ No requests found in onboarding_requests table.")
    exit(1)

req_id = req.data[0]["request_id"]
current_db_status = req.data[0]["status"]
print(f"▶️ Testing Request ID: {req_id} (Current DB Status: {current_db_status})")

# 2. Invoke Graph
config = {"configurable": {"thread_id": req_id}}
initial_state = {
    "request_id": req_id,
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
    "status": "pending_onboarding",
}

print("⏳ Running agent flow (fetch_context -> policy_rag -> llm_planning -> persist_plan)...")
result = onboarding_flow.invoke(initial_state, config=config)

# 3. Inspect Graph Checkpoint & Interruption
state_snapshot = onboarding_flow.get_state(config)
print("\n--- GRAPH EXECUTION SNAPSHOT ---")
print(f"Next pending node(s): {state_snapshot.next}")
print(f"Tasks paused at interrupt: {[task.name for task in state_snapshot.tasks]}")
print(f"Workflow State Status: {result.get('status')}")

# 4. Verify Database Persistence
run_check = (
    supabase.table("workflow_runs")
    .select("run_id, request_id, suggested_hardware, policy_citations")
    .eq("request_id", req_id)
    .execute()
)

print("\n--- SUPABASE VERIFICATION ---")
if run_check.data:
    print(f"✅ Row successfully written to 'workflow_runs' (Run ID: {run_check.data[0]['run_id']})")
    print(f"Suggested Hardware: {json.dumps(run_check.data[0]['suggested_hardware'], indent=2)}")
else:
    print("❌ No entry found in 'workflow_runs' table for this request.")