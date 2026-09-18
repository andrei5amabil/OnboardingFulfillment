from typing import Annotated, Any, Optional, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class OnboardingState(TypedDict):
    request_id: str
    employee_id: str
    candidate_data: dict[str, Any]
    sql_rules: list[dict[str, Any]]
    software_catalog: list[dict[str, Any]]
    citations: list[dict[str, Any]]
    suggested_licenses: list[dict[str, Any]]
    discretionary_licenses: list[dict[str, Any]]
    approved_discretionary_ids: list[str]
    suggested_hardware: dict[str, Any]
    policy_tags: list[str]
    flagged_exceptions: list[str]
    reviewed_by: Optional[str]
    is_approved: bool
    status: str
    attempt_count: int
    it_feedback: Optional[list[str]]
    review_action: Optional[str]