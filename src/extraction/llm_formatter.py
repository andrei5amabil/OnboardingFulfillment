import json
import logging
import os
from typing import Any, Union
import ollama
from pydantic import ValidationError
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from src.extraction.schemas import (
    DOCUMENT_SCHEMA_MAP,
    ContractExtractionSchema,
    DocumentType,
    HardwareDeliveryExtractionSchema,
    MedicalClearanceExtractionSchema,
    NationalIDExtractionSchema,
)

logger = logging.getLogger("uvicorn.error")

OLLAMA_JUDGE_MODEL = os.getenv("OLLAMA_MODEL", "granite4.2:3b")


class TrackCJudge:

    @staticmethod
    def _build_judge_prompt(
        doc_type: DocumentType,
        track_a_text: str,
        track_b_text: str,
    ) -> str:
        # Document-specific field hints to eliminate ambiguity
        field_hints = ""
        if doc_type == DocumentType.MEDICAL_CLEARANCE:
            field_hints = (
                "SPECIFIC MAPPINGS FOR MEDICAL CLEARANCE:\n"
                "- 'issue_date': Map from 'Data examinarii', 'Data emiterii', or examination/issue date. Do NOT leave null if a date is present.\n"
                "- 'medical_clearance_status': Set to true if 'APT' or 'APT PENTRU MUNCA', false if 'INAPT'."
            )
        elif doc_type == DocumentType.NATIONAL_ID:
            field_hints = (
                "SPECIFIC MAPPINGS FOR NATIONAL ID:\n"
                "- 'first_name': 'Prenume'\n"
                "- 'last_name': 'Nume'\n"
                "- 'national_id': 'CNP' or card number."
            )
        elif doc_type == DocumentType.CONTRACT:
            field_hints = (
                "SPECIFIC MAPPINGS FOR CONTRACT:\n"
                "- 'role': 'Functia' / 'Postul'\n"
                "- 'start_date': 'Data inceperii' / 'Data intrarii in vigoare' -> YYYY-MM-DD format."
            )
        elif doc_type == DocumentType.HARDWARE_DELIVERY:
            field_hints = (
                "SPECIFIC MAPPINGS FOR DELIVERY:\n"
                "- 'shipping_address': Street, city, postal code.\n"
                "- 'contact_phone': Phone number."
            )

        return f"""You are the Lead Document Arbitration Specialist.
Your task is to reconcile data extracted from two separate engines (Track A: Linear PDF/OCR Text and Track B: Visual Layout LLM) for a {doc_type.value.upper()}.

### ENGINE 1 (TRACK A: PDF TEXT / OCR STREAM)
{track_a_text or "[NO TEXT EXTRACTED BY TRACK A]"}

### ENGINE 2 (TRACK B: VISION MODEL EXTRACTION)
{track_b_text or "[NO TEXT EXTRACTED BY TRACK B]"}

### ARBITRATION RULES:
1. Reconcile minor OCR misspellings or diacritic corruptions (e.g., 'Å PTFENTRU' -> 'APT', meaning fit for work).
2. Dates: Convert all textual or regional date formats into ISO 8601 (YYYY-MM-DD). If a valid date exists in the source text, extract it and do NOT leave it null.
3. Names: Pick the clean, capitalization-corrected legal name, ignoring field labels like 'NUME', 'PRENUME', or 'SALARIAT'.
4. Medical Clearance: Determine clearance status strictly as a boolean:
   - True if 'APT' / 'FIT' / 'CLEARED'
   - False if 'INAPT' / 'UNFIT' or if the status is absent/unclear.
5. If an attribute is genuinely missing from both inputs, set it to null (or false for booleans).

{field_hints}

Return ONLY a valid JSON object matching the requested schema. No conversational filler."""
    
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
        HardwareDeliveryExtractionSchema,
        MedicalClearanceExtractionSchema,
    ]:
        """
        Reconciles Track A and Track B texts into a strictly validated Pydantic model.
        """
        schema_cls = DOCUMENT_SCHEMA_MAP[doc_type]
        judge_model = model or OLLAMA_JUDGE_MODEL

        prompt = cls._build_judge_prompt(doc_type, track_a_text, track_b_text)

        logger.info(f"Track C: Invoking Judge ({judge_model}) for doc_type='{doc_type.value}'")

        # 1. Grammar-constrained structured output via Ollama
        try:
            response = ollama.chat(
                model=judge_model,
                messages=[{"role": "user", "content": prompt}],
                format=schema_cls.model_json_schema(),
                options={
                    "temperature": 0.0,
                    "num_ctx": 4096,
                },
            )
            raw_content = response.get("message", {}).get("content", "").strip()
            validated_obj = schema_cls.model_validate_json(raw_content)
            return validated_obj
        except ValidationError as ve:
            logger.warning(f"Grammar validation failed on raw output ({ve}). Retrying with generic JSON mode.")
        except Exception as e:
            logger.warning(f"Track C constrained call failed: {e}. Retrying with generic JSON mode.")

        # 2. Fallback: Generic JSON mode
        fallback_prompt = (
            f"{prompt}\n\nRespond strictly with a JSON object adhering to the schema properties: "
            f"{list(schema_cls.model_fields.keys())}"
        )
        response = ollama.chat(
            model=judge_model,
            messages=[{"role": "user", "content": fallback_prompt}],
            format="json",
            options={"temperature": 0.0, "num_ctx": 4096},
        )
        raw_content = response.get("message", {}).get("content", "").strip()

        try:
            return schema_cls.model_validate_json(raw_content)
        except Exception as e:
            logger.error(f"Track C arbitration completely failed to produce valid schema: {e}\nRaw: {raw_content}")
            raise ValueError(f"Could not arbitrate document into {schema_cls.__name__}: {str(e)}")