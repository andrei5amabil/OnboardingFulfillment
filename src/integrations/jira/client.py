"""Minimal Jira Cloud REST API client.

Notes on API versions (Jira Cloud):
- Issue create/update/comment use REST API **v2** (``/rest/api/2/...``) so the
  ``description`` and comment ``body`` fields accept plain-text / Jira Wiki
  Markup strings. REST API v3 requires Atlassian Document Format (ADF) JSON and
  rejects plain strings with ``400 Bad Request`` for those fields.
- Status transitions use REST API **v3** (``/rest/api/3/issue/{key}/transitions``)
  and require a transition **id**, not a name. :meth:`JiraClient.transition_issue`
  resolves the id by first fetching the available transitions and matching the
  requested status name case-insensitively.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import requests
from dotenv import load_dotenv

logger = logging.getLogger("uvicorn.error")

env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path, override=False)

DEFAULT_TIMEOUT_SECONDS = 15.0


class JiraError(RuntimeError):
    """Raised when Jira returns an unexpected HTTP response or payload."""


class JiraNotConfiguredError(JiraError):
    """Raised when a Jira call is attempted without the required configuration."""


@dataclass
class JiraConfig:
    base_url: str = ""
    email: str = ""
    api_token: str = ""
    project_key: str = "IT"
    issue_type: str = "Task"
    subtask_issue_type: str = "Subtask"
    webhook_secret: str = ""
    logistics_assignee_account_id: str = ""
    timeout: float = DEFAULT_TIMEOUT_SECONDS

    @classmethod
    def from_env(cls) -> "JiraConfig":
        return cls(
            base_url=(os.getenv("JIRA_BASE_URL") or "").strip().rstrip("/"),
            email=(os.getenv("JIRA_EMAIL") or "").strip(),
            api_token=(os.getenv("JIRA_API_TOKEN") or "").strip(),
            project_key=(os.getenv("JIRA_PROJECT_KEY") or "IT").strip() or "IT",
            issue_type=(os.getenv("JIRA_ISSUE_TYPE") or "Task").strip() or "Task",
            subtask_issue_type=(
                os.getenv("JIRA_SUBTASK_ISSUE_TYPE") or "Subtask"
            ).strip() or "Subtask",
            webhook_secret=(os.getenv("JIRA_WEBHOOK_SECRET") or "").strip(),
            logistics_assignee_account_id=(
                os.getenv("JIRA_LOGISTICS_ASSIGNEE_ACCOUNT_ID") or ""
            ).strip(),
            timeout=float(os.getenv("JIRA_TIMEOUT_SECONDS") or DEFAULT_TIMEOUT_SECONDS),
        )

    @property
    def is_configured(self) -> bool:
        return bool(self.base_url and self.email and self.api_token and self.project_key)


class JiraClient:
    """Thin, synchronous Jira Cloud REST client used by the FastAPI backend."""

    def __init__(self, config: Optional[JiraConfig] = None, session: Optional[requests.Session] = None):
        self.config = config or JiraConfig.from_env()
        self.session = session or requests.Session()

    @property
    def is_configured(self) -> bool:
        return self.config.is_configured

    # ------------------------------------------------------------------ HTTP
    def _request(self, method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        if not self.config.is_configured:
            raise JiraNotConfiguredError(
                "Jira is not configured. Set JIRA_BASE_URL, JIRA_EMAIL, "
                "JIRA_API_TOKEN and JIRA_PROJECT_KEY."
            )

        url = f"{self.config.base_url}{endpoint}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        headers.update(kwargs.pop("headers", {}))

        try:
            response = self.session.request(
                method,
                url,
                auth=(self.config.email, self.config.api_token),
                headers=headers,
                timeout=self.config.timeout,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise JiraError(f"Jira request {method} {endpoint} failed: {exc}") from exc

        if response.status_code >= 400:
            raise JiraError(
                f"Jira {method} {endpoint} returned {response.status_code}: "
                f"{response.text[:500]}"
            )

        if response.status_code == 204 or not response.content:
            return {}
        try:
            return response.json()
        except ValueError:
            return {"raw": response.text}

    # --------------------------------------------------------------- Issues
    def create_issue(
        self,
        summary: str,
        description: str,
        issue_type: Optional[str] = None,
        labels: Optional[list[str]] = None,
        parent_key: Optional[str] = None,
        assignee_account_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create an issue (or sub-task when ``parent_key`` is provided)."""
        fields: dict[str, Any] = {
            "project": {"key": self.config.project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type or self.config.issue_type},
        }
        if labels:
            fields["labels"] = _sanitize_labels(labels)
        if parent_key:
            fields["parent"] = {"key": parent_key}
        if assignee_account_id:
            fields["assignee"] = {"accountId": assignee_account_id}

        return self._request("POST", "/rest/api/2/issue", json={"fields": fields})

    def create_subtask(
        self,
        parent_key: str,
        summary: str,
        description: str,
        labels: Optional[list[str]] = None,
        assignee_account_id: Optional[str] = None,
    ) -> dict[str, Any]:
        return self.create_issue(
            summary=summary,
            description=description,
            issue_type=self.config.subtask_issue_type,
            labels=labels,
            parent_key=parent_key,
            assignee_account_id=assignee_account_id,
        )

    def update_issue(
        self,
        issue_key: str,
        description: Optional[str] = None,
        summary: Optional[str] = None,
        labels: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        if description is not None:
            fields["description"] = description
        if summary is not None:
            fields["summary"] = summary
        if labels is not None:
            fields["labels"] = _sanitize_labels(labels)
        if not fields:
            return {}

        return self._request("PUT", f"/rest/api/2/issue/{issue_key}", json={"fields": fields})

    def get_issue(self, issue_key: str, fields: str = "status,summary") -> dict[str, Any]:
        return self._request("GET", f"/rest/api/3/issue/{issue_key}?fields={fields}")

    def get_myself(self) -> dict[str, Any]:
        """Return the authenticated Jira account (useful for setup checks)."""
        return self._request("GET", "/rest/api/3/myself")

    def add_comment(self, issue_key: str, body: str) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/rest/api/2/issue/{issue_key}/comment",
            json={"body": body},
        )

    # ----------------------------------------------------------- Transitions
    def get_transitions(self, issue_key: str) -> list[dict[str, Any]]:
        data = self._request("GET", f"/rest/api/3/issue/{issue_key}/transitions")
        return data.get("transitions") or []

    def ensure_status(self, issue_key: str, target_name: str) -> bool:
        """Transition only when the issue is not already in ``target_name``."""
        try:
            current = self.get_issue(issue_key)
            current_status = str(
                ((current.get("fields") or {}).get("status") or {}).get("name") or ""
            ).strip()
            if current_status.casefold() == (target_name or "").strip().casefold():
                return True
        except JiraError as exc:
            logger.debug("Could not read current status for %s: %s", issue_key, exc)

        return self.transition_issue(issue_key, target_name)

    def transition_issue(self, issue_key: str, target_name: str, raise_on_missing: bool = False) -> bool:
        """Move an issue to the transition whose name matches ``target_name``.

        Jira's transitions endpoint requires an id, so this first fetches the
        currently available transitions and matches the requested status name
        case-insensitively.
        """
        target = (target_name or "").strip().casefold()
        transitions = self.get_transitions(issue_key)

        for transition in transitions:
            name = str(transition.get("name") or "").strip()
            if name.casefold() == target:
                self._request(
                    "POST",
                    f"/rest/api/3/issue/{issue_key}/transitions",
                    json={"transition": {"id": transition["id"]}},
                )
                logger.info("Jira issue %s transitioned to '%s'.", issue_key, name)
                return True

        available = [str(t.get("name") or "?") for t in transitions]
        message = (
            f"No Jira transition named '{target_name}' is available for {issue_key}. "
            f"Available transitions: {available}"
        )
        if raise_on_missing:
            raise JiraError(message)
        logger.warning(message)
        return False

    # ----------------------------------------------------------------- Utils
    def browse_url(self, issue_key: str) -> str:
        return f"{self.config.base_url}/browse/{issue_key}" if self.config.base_url else ""


def _sanitize_labels(labels: list[str]) -> list[str]:
    """Jira labels cannot contain spaces and are case-insensitive."""
    cleaned: list[str] = []
    for label in labels:
        value = str(label).strip().lower().replace(" ", "-")
        value = re.sub(r"[^a-z0-9_-]+", "-", value).strip("-")
        if value and value not in cleaned:
            cleaned.append(value)
    return cleaned


def adf_to_text(node: Any) -> str:
    """Flatten an Atlassian Document Format node into plain text.

    Jira Cloud sends comment bodies as ADF for REST API v3 events. This helper
    keeps the webhook parser readable without pulling in the full ADF spec.
    """
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return " ".join(part for part in (adf_to_text(item) for item in node) if part).strip()
    if not isinstance(node, dict):
        return str(node)

    node_type = node.get("type")
    if node_type == "text":
        return str(node.get("text") or "")
    if node_type in {"hardBreak", "rule"}:
        return "\n"
    if node_type == "mention":
        attrs = node.get("attrs") or {}
        return str(attrs.get("text") or attrs.get("displayName") or "")
    if node_type in {"emoji"}:
        attrs = node.get("attrs") or {}
        return str(attrs.get("text") or attrs.get("shortName") or "")

    content = adf_to_text(node.get("content") or [])
    if node_type in {"paragraph", "heading", "listItem", "codeBlock", "blockquote", "panel"}:
        return f"{content}\n".strip()
    return content


jira_client = JiraClient()
