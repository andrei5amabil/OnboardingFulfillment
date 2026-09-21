from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional
import re


@dataclass
class ValidationAlert:
    severity: str  # "critical", "warning", "info"
    field: str
    message: str


def validate_romanian_cnp(cnp: str | None) -> tuple[bool, str]:
    """Validates length, character set, and the MOD-11 control digit of a Romanian CNP."""
    if not cnp:
        return False, "CNP is missing."

    clean_cnp = re.sub(r"\s+", "", cnp).strip()
    if len(clean_cnp) != 13 or not clean_cnp.isdigit():
        return False, f"CNP '{clean_cnp}' must be exactly 13 digits."

    # Standard Romanian CNP validation key
    CONTROL_KEY = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    digits = [int(d) for d in clean_cnp]

    checksum = sum(d * k for d, k in zip(digits[:12], CONTROL_KEY)) % 11
    expected_control = 1 if checksum == 10 else checksum

    if digits[12] != expected_control:
        return False, f"CNP '{clean_cnp}' failed mathematical checksum verification."

    return True, "CNP is valid."


def normalize_name_tokens(name: str | None) -> set[str]:
    """Strips whitespace, punctuation, and lowercases tokens for order-agnostic comparison."""
    if not name:
        return set()
    cleaned = re.sub(r"[^a-zA-Z\s\-]", "", name.lower())
    return {token for token in cleaned.replace("-", " ").split() if len(token) > 1}


def validate_cross_documents(
    contract_data: dict,
    national_id_data: dict,
    medical_data: dict,
) -> list[ValidationAlert]:
    """Cross-references extracted entities across all scanned documents."""
    alerts: list[ValidationAlert] = []

    c_cnp = (contract_data.get("national_id") or "").strip()
    id_cnp = (national_id_data.get("national_id") or "").strip()

    # 1. CNP Discrepancy & Checksum
    if id_cnp:
        is_valid, reason = validate_romanian_cnp(id_cnp)
        if not is_valid:
            alerts.append(ValidationAlert("critical", "national_id", f"National ID Card: {reason}"))

    if c_cnp and id_cnp:
        if c_cnp != id_cnp:
            alerts.append(
                ValidationAlert(
                    "critical",
                    "national_id",
                    f"CRITICAL DISCREPANCY: CNP on Contract ('{c_cnp}') does NOT match National ID ('{id_cnp}').",
                )
            )

    # 2. Name Consistency (Contract vs National ID)
    c_name_tokens = normalize_name_tokens(f"{contract_data.get('first_name', '')} {contract_data.get('last_name', '')}")
    id_name_tokens = normalize_name_tokens(f"{national_id_data.get('first_name', '')} {national_id_data.get('last_name', '')}")

    if c_name_tokens and id_name_tokens:
        if not c_name_tokens.intersection(id_name_tokens):
            alerts.append(
                ValidationAlert(
                    "critical",
                    "name",
                    f"Name mismatch: Contract name ('{contract_data.get('first_name')} {contract_data.get('last_name')}') "
                    f"does not match National ID ('{national_id_data.get('first_name')} {national_id_data.get('last_name')}').",
                )
            )
        elif c_name_tokens != id_name_tokens:
            alerts.append(
                ValidationAlert(
                    "warning",
                    "name",
                    "Minor name variation detected between Contract and National ID (e.g., middle name omitted).",
                )
            )

    # 3. Medical Clearance Gatekeeper
    med_status = medical_data.get("medical_clearance_status")
    if med_status is False:
        alerts.append(
            ValidationAlert(
                "critical",
                "medical_clearance",
                "COMPLIANCE GATE: Medical certificate indicates candidate is UNFIT or clearance is unconfirmed.",
            )
        )

    # 4. Temporal Sanity (Medical Exam vs Contract Start Date)
    exam_date = medical_data.get("issue_date")
    start_date = contract_data.get("start_date")

    if exam_date and start_date:
        if isinstance(exam_date, str):
            exam_date = date.fromisoformat(exam_date)
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)

        # Clearance older than 180 days is legally stale
        if (start_date - exam_date) > timedelta(days=180):
            alerts.append(
                ValidationAlert(
                    "warning",
                    "medical_clearance_date",
                    f"Medical clearance examination date ({exam_date}) is more than 6 months prior to start date ({start_date}).",
                )
            )
        elif exam_date > (start_date + timedelta(days=14)):
            alerts.append(
                ValidationAlert(
                    "warning",
                    "medical_clearance_date",
                    f"Medical clearance date ({exam_date}) is set well after the employment start date ({start_date}).",
                )
            )

    return alerts