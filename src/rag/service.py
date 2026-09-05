from typing import Any
from src.rag.retriever import PolicyRetriever

retriever = None

def get_retriever():
    global retriever
    if retriever is None:
        retriever = PolicyRetriever()
    return retriever

def retrieve_onboarding_policies(req: dict[str, Any]) -> list[dict[str, Any]]:
    work_location = req.get("work_location", "on-site")
    department = req.get("department", "")
    role = req.get("role", "")
    notes = (req.get("notes") or "").strip()

    # Targeted query passes
    queries = [
        f"hardware asset allocation logistics delivery work location {work_location}",
        f"network access vpn enclave profile department {department} role {role} work location {work_location}",
    ]
    if notes:
        queries.append(f"{notes}")

    seen_parents = set()
    citations = []

    for q in queries:
        matches = get_retriever().retrieve(query=q, top_k_candidates=8, final_top_k=2)
        for doc in matches:
            if doc["parent_id"] not in seen_parents:
                seen_parents.add(doc["parent_id"])
                citations.append(doc)

    return citations


def build_reasoning_prompt(req: dict[str, Any], sql_rules: list[dict[str, Any]], citations: list[dict[str, Any]]) -> str:
    policy_context = "\n\n".join([
        f"### {doc['policy_name']} - {doc['section_title']} (Clauses: {', '.join(doc['clause_tags'])})\n{doc['content']}"
        for doc in citations
    ])

    return f"""You are the Enterprise Onboarding Orchestrator. 
Analyze the candidate profile, deterministic database entitlements, and internal compliance policies to produce a structured plan.

### CANDIDATE PROFILE
- Employee ID: {req.get('employee_id')}
- Role: {req.get('role')}
- Department: {req.get('department')}
- Work Location: {req.get('work_location')}
- Notes: {req.get('notes') or "None"}

### DETERMINISTIC SQL ENTITLEMENTS
{sql_rules}

### RETRIEVED POLICIES
{policy_context}

Return strictly a valid JSON object."""