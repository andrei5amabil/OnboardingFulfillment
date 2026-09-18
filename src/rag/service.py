from typing import Any
from src.rag.retriever import PolicyRetriever
import threading

retriever = None
_retriever_lock = threading.Lock()

def get_retriever():
    global retriever
    if retriever is None:
        with _retriever_lock:
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
        f"### {doc.get('policy_name', 'Policy')} - {doc.get('section_title', 'Section')} "
        f"(Clauses: {', '.join(doc.get('clause_tags', []))})\n{doc.get('content', '')}"
        for doc in citations
    ])

    assigned_tools = ", ".join([
        (r.get("software_products") or {}).get("name", "Unknown")
        for r in sql_rules
    ]) or "Standard office suite"

    return f"""You are the Enterprise Hardware & Compliance Planning Agent.
Your objective is to determine hardware provisioning, peripherals, shipping requirements, and compliance flags for a new hire.

### CANDIDATE PROFILE
- Employee ID: {req.get('employee_id')}
- Role: {req.get('role')}
- Department: {req.get('department')}
- Work Location: {req.get('work_location')} (e.g., remote, hybrid, onsite)
- Assigned Baseline Tools: {assigned_tools}

### RETRIEVED GOVERNANCE & HARDWARE POLICIES
{policy_context}

### PLANNING INSTRUCTIONS
1. **Laptop Provisioning**: Choose an appropriate laptop tier based on the role and department policies (e.g., high-performance developer workstation vs. standard enterprise laptop).
2. **Peripherals**: Specify necessary peripherals based on policies and role (e.g., external monitors, dock, keyboard, mouse).
3. **Shipping Required**: Set to `true` if the candidate is remote or hybrid requiring home delivery; set to `false` if strictly onsite.
4. **Policy Citations & Exceptions**: List applicable policy codes or clause tags from the retrieved text, and flag any compliance exceptions (e.g., contractors requiring non-standard equipment or elevated review).

Do NOT assign or suggest software licenses. Output strictly valid JSON matching the schema."""