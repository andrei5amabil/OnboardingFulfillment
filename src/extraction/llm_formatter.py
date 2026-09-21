import json
import logging
import os
import re
import time
from typing import Union
import ollama
from pydantic import ValidationError

from src.extraction.schemas import (
    DOCUMENT_SCHEMA_MAP,
    ContractExtractionSchema,
    DocumentType,
    MedicalClearanceExtractionSchema,
    NationalIDExtractionSchema,
)

logger = logging.getLogger("uvicorn.error")
OLLAMA_JUDGE_MODEL = os.getenv("OLLAMA_JUDGE_MODEL", "qwen2.5:3b")


def extract_json_block(text: str) -> str:
    """Extracts the outermost valid JSON object from a string, stripping markdown or thinking text."""
    text = text.strip()
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


class TrackCJudge:

    @staticmethod
    def _build_judge_prompt(
        doc_type: DocumentType,
        track_a_text: str,
        track_b_text: str,
    ) -> str:
        return f"""You are a precise data extraction specialist.
Extract structured JSON matching the requested schema from the document streams below for a {doc_type.value.upper()}.

### SOURCE 1 (PDF TEXT / OCR):
{track_a_text or "[NO TEXT]"}

### SOURCE 2 (VISION MODEL OUTPUT):
{track_b_text or "[NO TEXT]"}

### FIELD EXTRACTION RULES:
1. For CONTRACT documents:
   - "Employee: <Full Name>" -> Split into 'first_name' and 'last_name' (e.g., "Employee: Andreea Dumitrescu" -> first_name: "Andreea", last_name: "Dumitrescu").
   - "Job Title / Role: <Title>" -> Extract as 'role' (e.g., "UI/UX Designer").
   - "Department: <Dept>" -> Extract exact string as 'department'.
   - "Start Date / Effective Date: <Date>" -> Extract as 'start_date' (YYYY-MM-DD).
   - "Reporting Manager ID: <ID>" -> Extract as 'manager_id'.
   - "Delivery / Residential Address: <Addr>" -> Extract as 'shipping_address'.
   - "Contact Phone Number: <Phone>" -> Extract as 'contact_phone'.

2. For NATIONAL ID documents:
   - Extract 'first_name', 'last_name', and the 13-digit 'national_id' (CNP).

3. For MEDICAL CLEARANCE documents:
   - Extract 'issue_date' (YYYY-MM-DD).
   - 'medical_clearance_status': true if 'FIT FOR WORK', 'CLEARED', or 'APT' is checked/stated. Otherwise false.

4. If an attribute is completely missing from the text, set it to null. Never invent placeholders.
5. Return strictly valid JSON adhering to the schema."""

    @classmethod
    def arbitrate(
        cls,
        doc_type: DocumentType,
        track_a_text: str,
        track_b_text: str,
        model: str | None = None,
    ) -> Union[
        ContractExtractionSchema,
        NationalIDExtractionSchema,
        MedicalClearanceExtractionSchema,
    ]:
        schema_cls = DOCUMENT_SCHEMA_MAP[doc_type]
        judge_model = model or OLLAMA_JUDGE_MODEL
        prompt = cls._build_judge_prompt(doc_type, track_a_text, track_b_text)

        logger.info(f"\n--- ⚖️ [TRACK C ARBITRATION] Model='{judge_model}' | Target='{schema_cls.__name__}' ---")
        t0 = time.time()

        # Try 1: Structured grammar constraint
        try:
            response = ollama.chat(
                model=judge_model,
                messages=[{"role": "user", "content": prompt}],
                format=schema_cls.model_json_schema(),
                options={"temperature": 0.0, "num_ctx": 2048},
            )
            msg = response.get("message", {})
            # Read content, with fallback to thinking if content is empty
            raw_content = msg.get("content", "").strip() or msg.get("thinking", "").strip()
            raw_json = extract_json_block(raw_content)

            logger.info(f"   └── Track C completed in {time.time() - t0:.2f}s")
            logger.info(f">>> [RAW TRACK C JSON]:\n{raw_json}")

            validated = schema_cls.model_validate_json(raw_json)
            logger.info(f">>> ✅ [VALIDATED {schema_cls.__name__}]:\n{validated.model_dump_json(indent=2)}\n" + "=" * 60)
            return validated

        except Exception as e:
            logger.warning(f"   └── ⚠️ Grammar parsing failed ({e}). Retrying in generic JSON mode...")

        # Try 2: Generic JSON mode
        fallback_prompt = (
            f"{prompt}\n\nRespond ONLY with a JSON object containing keys: {list(schema_cls.model_fields.keys())}"
        )
        try:
            response = ollama.chat(
                model=judge_model,
                messages=[{"role": "user", "content": fallback_prompt}],
                format="json",
                options={"temperature": 0.0, "num_ctx": 2048},
            )
            msg = response.get("message", {})
            raw_content = msg.get("content", "").strip() or msg.get("thinking", "").strip()
            raw_json = extract_json_block(raw_content)
            logger.info(f">>> [FALLBACK JSON]:\n{raw_json}")

            validated = schema_cls.model_validate_json(raw_json)
            logger.info(f">>> ✅ [VALIDATED (FALLBACK)]:\n{validated.model_dump_json(indent=2)}\n" + "=" * 60)
            return validated
        except Exception as e:
            logger.error(f"❌ Track C arbitration completely failed for {doc_type.value}: {e}")
            # Fallback to an empty instance of the schema to avoid crashing the entire pipeline
            return schema_cls()