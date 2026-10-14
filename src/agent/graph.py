from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src.agent.nodes import (
    execute_provisioning_node,
    fetch_context_node,
    finalize_workflow_node,
    handle_max_retries_node,
    human_approval_gate_node,
    llm_planning_node,
    persist_plan_node,
    policy_rag_node,
    discretionary_licensing_node,
)
from src.agent.state import OnboardingState

MAX_ATTEMPTS = 3


def route_after_review(state: OnboardingState) -> str:
    """Routes execution based on human approval, cycle count, or escalation limits."""
    if state.get("is_approved"):
        return "execute_provisioning"

    if state.get("review_action") == "regenerate":
        if state.get("attempt_count", 1) <= MAX_ATTEMPTS:
            return "llm_planning"
        return "handle_max_retries"

    return "handle_max_retries"


builder = StateGraph(OnboardingState)

# 1. Register nodes
builder.add_node("fetch_context", fetch_context_node)
builder.add_node("policy_rag", policy_rag_node)
builder.add_node("llm_planning", llm_planning_node)
builder.add_node("discretionary_licensing", discretionary_licensing_node)
builder.add_node("persist_plan", persist_plan_node)
builder.add_node("human_approval_gate", human_approval_gate_node)
builder.add_node("handle_max_retries", handle_max_retries_node)
builder.add_node("execute_provisioning", execute_provisioning_node)
builder.add_node("finalize_workflow", finalize_workflow_node)

# 2. Linear initialization
builder.add_edge(START, "fetch_context")
builder.add_edge("fetch_context", "policy_rag")
builder.add_edge("policy_rag", "llm_planning")
builder.add_edge("llm_planning", "discretionary_licensing")
builder.add_edge("discretionary_licensing", "persist_plan")
builder.add_edge("persist_plan", "human_approval_gate")

# 3. Dynamic HITL cyclic routing (Keys must match route_after_review return values)
builder.add_conditional_edges(
    "human_approval_gate",
    route_after_review,
    {
        "execute_provisioning": "execute_provisioning",
        "llm_planning": "llm_planning",
        "handle_max_retries": "handle_max_retries",
    },
)

# 4. Deterministic completion and terminal paths
builder.add_edge("execute_provisioning", "finalize_workflow")
builder.add_edge("finalize_workflow", END)
builder.add_edge("handle_max_retries", END)

# In-memory checkpointer tracks paused thread states across invocations
checkpointer = MemorySaver()
onboarding_flow = builder.compile(checkpointer=checkpointer)