from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Optional, Union
import time

from src.extraction.preprocessing import DocumentPreprocessor
from src.extraction.schemas import (
    ContractExtractionSchema,
    DocumentType,
    ExtractionResponse,
    MedicalClearanceExtractionSchema,
    NationalIDExtractionSchema,
)
from src.extraction.parse_ocr import TrackAExtractor
from src.extraction.vllm_extract import TrackBExtractor
from src.extraction.llm_formatter import TrackCJudge

MODEL_SKIP_THRESHOLD = 200

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
        t0 = time.time()
        logger.info("\n" + "=" * 70)
        logger.info(f"🚀 [PIPELINE START] File='{filename}' | Type='{doc_type.value}' | MIME='{content_type}'")
        logger.info("=" * 70)

        # 1. Validation & Page Normalization
        pages = DocumentPreprocessor.validate_and_load(
            file_bytes=file_bytes,
            content_type=content_type,
            filename=filename,
        )

        # 2. Check for Rich Digital Text Layer (Fast-Path)
        total_digital_chars = sum(len(p.text.strip()) for p in pages)
        is_digital_document = total_digital_chars >= MODEL_SKIP_THRESHOLD

        track_a_text = ""
        track_b_text = ""

        if is_digital_document:
            logger.info(
                f"Fast-path triggered for '{filename}': {total_digital_chars} digital chars detected. "
                "Skipping Vision LLM (Track B)."
            )
            # Track A extracts the native digital text layer in < 50ms
            track_a_text = TrackAExtractor.extract(pages)
            track_b_text = "[DIGITAL DOCUMENT: Track B vision bypassed to optimize latency]"
        else:
            logger.info(f"Visual document detected for '{filename}'. Running Track A (OCR) & Track B (Vision).")
            # Concurrently run OCR and Vision for scans/photos
            with ThreadPoolExecutor(max_workers=2) as executor:
                future_a = executor.submit(TrackAExtractor.extract, pages)
                future_b = executor.submit(
                    TrackBExtractor.extract,
                    pages=pages,
                    doc_type=doc_type,
                    model=vision_model,
                )
                track_a_text = future_a.result()
                track_b_text = future_b.result()

        # 3. Track C: Judge LLM Arbitration
        validated_data = TrackCJudge.arbitrate(
            doc_type=doc_type,
            track_a_text=track_a_text,
            track_b_text=track_b_text,
            model=judge_model,
        )

        # 4. Confidence / Sanity checks
        flags = []
        if doc_type == DocumentType.MEDICAL_CLEARANCE:
            if not validated_data.medical_clearance_status:
                flags.append("WARNING: Candidate is marked as NOT medically cleared.")
            if not validated_data.issue_date:
                flags.append("NOTICE: Examination date could not be detected.")
        elif doc_type == DocumentType.NATIONAL_ID:
            if not validated_data.national_id:
                flags.append("WARNING: CNP / National ID number could not be extracted.")
        elif doc_type == DocumentType.CONTRACT:
            if not validated_data.role:
                flags.append("NOTICE: Role / Function was not clearly identified.")
            if not validated_data.start_date:
                flags.append("NOTICE: Start date was not clearly identified.")

        total_elapsed = time.time() - t0
        logger.info(f"🏁 [PIPELINE FINISHED] Completed in {total_elapsed:.2f}s | Warnings: {flags}")
        logger.info("=" * 70 + "\n")
        
        return ExtractionResponse(
            status="success",
            document_type=doc_type,
            filename=filename,
            confidence_flags=flags,
            data=validated_data,
        )