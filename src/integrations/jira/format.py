"""Render onboarding plans as Jira Wiki Markup (REST API v2 plain text)."""

from __future__ import annotations

import json
from typing import Any, Optional

from src.integrations.jira.workflow import (
    STATUS_PENDING_APPROVAL,
    STATUS_NEEDS_REVISION,
    STATUS_APPROVED,
)


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (list, tuple)):
        return ", ".join(part for part in (_text(item) for item in value) if part)
    if isinstance(value, dict):
        if not value:
            return ""
        try:
            return json.dumps(value, ensure_ascii=False)
        except TypeError:
            return str(value)
    return str(value).strip()


def _cell(value: Any) -> str:
    """Escape a value for a Jira Wiki Markup table cell."""
    return _text(value).replace("|", "\\|").replace("\n", " ").strip()


def _table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["||" + "||".join(headers) + "||"]
    for row in rows:
        lines.append("|" + "|".join(_cell(cell) for cell in row) + "|")
    return lines


def _candidate_name(candidate: dict[str, Any]) -> str:
    first = str(candidate.get("first_name") or "").strip()
    last = str(candidate.get("last_name") or "").strip()
    return " ".join(part for part in (first, last) if part) or "New Hire"


def build_ticket_summary(state: dict[str, Any]) -> str:
    candidate = state.get("candidate_data") or {}
    name = _candidate_name(candidate)
    role = str(candidate.get("role") or "").strip()
    return f"Onboarding - {name} ({role})" if role else f"Onboarding - {name}"


def build_onboarding_ticket_description(state: dict[str, Any]) -> str:
    """Build the parent ticket description for the current plan attempt."""
    candidate = state.get("candidate_data") or {}
    name = _candidate_name(candidate)
    request_id = str(state.get("request_id") or candidate.get("request_id") or "")
    employee_id = str(state.get("employee_id") or candidate.get("employee_id") or "")
    attempt = state.get("attempt_count", 1)

    lines: list[str] = [
        f"h2. Onboarding Plan - {name}",
        "",
        f"*Request:* {request_id}",
        f"*Employee:* {employee_id}",
        f"*Department:* {_text(candidate.get('department'))}",
        f"*Role:* {_text(candidate.get('role'))}",
        f"*Start date:* {_text(candidate.get('start_date'))}",
        f"*Work location:* {_text(candidate.get('work_location'))}",
        f"*Plan attempt:* {_text(attempt)}",
        f"*Status:* {_text(state.get('status') or STATUS_PENDING_APPROVAL)}",
        "",
    ]

    _append_license_section(lines, state)
    _append_discretionary_section(lines, state)
    _append_hardware_section(lines, state)
    _append_policy_section(lines, state)
    _append_exceptions_section(lines, state)

    lines.extend(
        [
            "h3. Approval",
            "Approve or request a revision from the Onboarding Portal, or transition this "
            f"issue to *{STATUS_APPROVED}* / *{STATUS_NEEDS_REVISION}* and leave a comment.",
            "",
            "_This ticket is synchronized with the Onboarding Portal by the onboarding agent._",
        ]
    )
    return "\n".join(lines)


def _append_license_section(lines: list[str], state: dict[str, Any]) -> None:
    licenses = state.get("suggested_licenses") or []
    lines.append("h3. Suggested licenses")
    if not licenses:
        lines.extend(["No mandatory software rules matched this hire.", ""])
        return

    rows: list[list[Any]] = []
    for rule in licenses:
        product = rule.get("software_products") or {}
        rows.append(
            [
                product.get("name") or rule.get("name"),
                product.get("vendor") or rule.get("vendor"),
                product.get("license_type") or rule.get("license_type"),
                rule.get("access_level") or "standard",
                rule.get("is_mandatory"),
                rule.get("requires_approval"),
            ]
        )
    lines.extend(
        _table(
            ["Product", "Vendor", "Type", "Access level", "Mandatory", "Approval required"],
            rows,
        )
    )
    lines.append("")


def _append_discretionary_section(lines: list[str], state: dict[str, Any]) -> None:
    proposals = state.get("discretionary_licenses") or []
    lines.append("h3. Discretionary licenses")
    if not proposals:
        lines.extend(["No discretionary software was requested.", ""])
        return

    for item in proposals:
        name = item.get("name") or item.get("product_id") or "Unknown product"
        product_id = item.get("product_id")
        suffix = f" ({product_id})" if product_id else ""
        justification = str(item.get("justification") or "No justification provided.").strip()
        lines.append(f"* *{name}*{suffix} - {justification}")
    lines.append("")


def _append_hardware_section(lines: list[str], state: dict[str, Any]) -> None:
    hardware = state.get("suggested_hardware") or {}
    lines.append("h3. Suggested hardware")
    if not hardware:
        lines.extend(["No hardware recommendation was generated.", ""])
        return

    laptop = hardware.get("laptop")
    if laptop:
        lines.append(f"* *Laptop:* {_text(laptop)}")

    peripherals = hardware.get("peripherals") or []
    if peripherals:
        lines.append(f"* *Peripherals:* {_text(peripherals)}")

    lines.append(f"* *Shipping required:* {_text(bool(hardware.get('shipping_required')))}")

    # Surface any additional hardware attributes without assuming a schema.
    known = {"laptop", "peripherals", "shipping_required"}
    for key, value in hardware.items():
        if key in known or value in (None, "", [], {}):
            continue
        pretty_key = key.replace("_", " ").capitalize()
        lines.append(f"* *{pretty_key}:* {_text(value)}")
    lines.append("")


def _append_policy_section(lines: list[str], state: dict[str, Any]) -> None:
    tags = list(state.get("policy_tags") or [])
    citations = state.get("citations") or []

    lines.append("h3. Policy citations")
    if not tags and not citations:
        lines.extend(["No policy citations were retrieved.", ""])
        return

    if tags:
        lines.append(f"* *Clauses:* {_text(tags)}")
    for citation in citations:
        code = citation.get("policy_code") or citation.get("code") or "Policy"
        section = citation.get("section_title") or citation.get("section") or ""
        lines.append(f"* {code} - {section}".rstrip(" -"))
    lines.append("")


def _append_exceptions_section(lines: list[str], state: dict[str, Any]) -> None:
    exceptions = state.get("flagged_exceptions") or []
    lines.append("h3. Flagged exceptions")
    if not exceptions:
        lines.extend(["No exceptions flagged.", ""])
        return
    for exception in exceptions:
        lines.append(f"* {_text(exception)}")
    lines.append("")


def build_logistics_subtask_description(state: dict[str, Any]) -> str:
    """Description for the Facilities/Logistics sub-task."""
    candidate = state.get("candidate_data") or {}
    hardware = state.get("suggested_hardware") or {}
    name = _candidate_name(candidate)

    lines = [
        f"h2. Hardware shipment - {name}",
        "",
        f"*Request:* {_text(state.get('request_id') or candidate.get('request_id'))}",
        f"*Employee:* {_text(state.get('employee_id') or candidate.get('employee_id'))}",
        f"*Laptop tier:* {_text(hardware.get('laptop'))}",
        f"*Peripherals:* {_text(hardware.get('peripherals'))}",
        f"*Shipping address:* {_text(candidate.get('shipping_address'))}",
        f"*Contact phone:* {_text(candidate.get('contact_phone'))}",
        f"*Start date:* {_text(candidate.get('start_date'))}",
        f"*Work location:* {_text(candidate.get('work_location'))}",
        "",
        "Please prepare and ship the equipment listed above. Update this sub-task with the "
        "tracking number once dispatched.",
    ]
    return "\n".join(lines)


def build_review_comment(action: str, reviewer: str, note: Optional[str] = None) -> str:
    if action == "approve":
        comment = f"Approved by {reviewer} via Onboarding Portal."
    else:
        comment = f"Revision requested by {reviewer} via Onboarding Portal."
    if note:
        comment = f"{comment}\n\n{note.strip()}"
    return comment
