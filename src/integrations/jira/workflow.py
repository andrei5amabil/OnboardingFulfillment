"""Shared Jira workflow constants and mapping helpers."""

from __future__ import annotations

from typing import Any, Optional

# Statuses expected in the Jira "IT" project workflow.
STATUS_PENDING_APPROVAL = "Pending Approval"
STATUS_APPROVED = "Approved"
STATUS_NEEDS_REVISION = "Needs Revision"
STATUS_IN_PROGRESS = "In Progress"
STATUS_DONE = "Done"

_APPROVE_STATUSES = {"approved", "approve"}
_REVISION_STATUSES = {"needs revision", "need revision", "revision requested", "rejected"}


def map_status_to_action(status_name: Optional[str]) -> Optional[str]:
    """Map a Jira status to a LangGraph review action.

    Returns ``"approve"``, ``"regenerate"`` or ``None`` when the status is not
    an approval-gate decision (e.g. ``In Progress`` or ``Done``).
    """
    normalized = (status_name or "").strip().casefold()
    if normalized in _APPROVE_STATUSES:
        return "approve"
    if normalized in _REVISION_STATUSES:
        return "regenerate"
    return None


def is_service_account(author: Any, service_email: str, service_account_id: str = "") -> bool:
    """Return True when a Jira event was authored by the integration account.

    Portal-initiated transitions are performed with the API token account. Their
    Jira webhooks must be ignored, otherwise the graph would be resumed twice
    (once by the portal, once by the webhook).
    """
    if not isinstance(author, dict):
        return False

    email = str(author.get("emailAddress") or "").strip().casefold()
    account_id = str(author.get("accountId") or "").strip()

    if service_email and email and email == service_email.strip().casefold():
        return True
    if service_account_id and account_id and account_id == service_account_id.strip():
        return True
    return False
