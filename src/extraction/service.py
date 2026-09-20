from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Optional, Union

from src.extraction.preprocessing import DocumentPreprocessor
from src.extraction.schemas import (
    ContractExtractionSchema,
    DocumentType,
    ExtractionResponse,
    HardwareDeliveryExtractionSchema,
    MedicalClearanceExtractionSchema,
    NationalIDExtractionSchema,
)
from src.extraction.parse_ocr import TrackAExtractor
from src.extraction.vllm_extract import TrackBExtractor
from src.extraction.llm_formatter import TrackCJudge

logger = logging.getLogger("uvicorn.error")


class DocumentExtractionService:

    @classmethod
    def process_document(
        cls,
        file_bytes: bytes,
        filename: str,
        doc_type: DocumentType,
        content_type: Optional[str] = None,
        vision_model: Optional[str] = None,
        judge_model: Optional[str] = None,
    ) -> ExtractionResponse:
        """Orchestrates Preprocessing -> Concurrent Track A (OCR) & Track B (Vision) -> Track C (Arbitration)."""
        logger.info(f"Starting extraction for '{filename}' as doc_type='{doc_type.value}'")

        # 1. Validation & Page Normalization
        pages = DocumentPreprocessor.validate_and_load(
            file_bytes=file_bytes,
            content_type=content_type,
            filename=filename,
        )

        # 2. Concurrently execute Track A (CPU/OCR) and Track B (GPU/Vision)
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_track_a = executor.submit(TrackAExtractor.extract, pages)
            future_track_b = executor.submit(
                TrackBExtractor.extract,
                pages=pages,
                doc_type=doc_type,
                model=vision_model,
            )

            track_a_text = future_track_a.result()
            track_b_text = future_track_b.result()

        logger.debug(f"Track A Result (Chars: {len(track_a_text)})")
        logger.debug(f"Track B Result (Chars: {len(track_b_text)})")

        # 3. Track C: Judge LLM Arbitration
        validated_data = TrackCJudge.arbitrate(
            doc_type=doc_type,
            track_a_text=track_a_text,
            track_b_text=track_b_text,
            model=judge_model,
        )

        # 4. Confidence / Sanity checks (Non-blocking warnings for HR)
        flags = []
        if doc_type == DocumentType.MEDICAL_CLEARANCE:
            if not validated_data.medical_clearance_status:
                flags.append("WARNING: Candidate is marked as NOT medically cleared.")
            if not validated_data.issue_date:
                flags.append("NOTICE: Examination/Issue date could not be detected.")

        elif doc_type == DocumentType.NATIONAL_ID:
            if not validated_data.national_id:
                flags.append("WARNING: CNP / National ID number could not be extracted.")

        elif doc_type == DocumentType.CONTRACT:
            if not validated_data.role:
                flags.append("NOTICE: Role / Function was not clearly identified.")
            if not validated_data.start_date:
                flags.append("NOTICE: Start date was not clearly identified.")

        return ExtractionResponse(
            status="success",
            document_type=doc_type,
            filename=filename,
            confidence_flags=flags,
            data=validated_data,
        )