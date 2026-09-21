import base64
import io
import logging
import os
from typing import Optional
import ollama
from PIL import Image
import time

from src.extraction.preprocessing import DocumentPage
from src.extraction.schemas import DocumentType
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

logger = logging.getLogger("uvicorn.error")

OLLAMA_VISION_MODEL = os.getenv("OLLAMA_VISION_MODEL", "glm-ocr:latest")

# Maximum number of pages to feed into the vision model per document
MAX_VISION_PAGES = 2

class TrackBExtractor:

    @staticmethod
    def _image_to_base64(img: Image.Image) -> str:
        """Encodes a PIL Image to a JPEG base64 string for the Ollama API."""
        buffer = io.BytesIO()
        # Save as JPEG with 85 quality to keep payload lightweight without losing text sharpness
        img.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    @staticmethod
    def _build_vision_prompt(doc_type: DocumentType) -> str:
        """Builds a targeted extraction prompt based on the specific document category."""
        base_instruction = (
            "You are an expert document inspector. Analyze the provided document image(s) carefully. "
            "Transcribe the labeled field values clearly and accurately. "
            "Extract each field once without repeating text.\n\n"
        )

        if doc_type == DocumentType.CONTRACT:
            return base_instruction + (
                "Document Type: EMPLOYMENT CONTRACT / AGREEMENT\n"
                "Extract the following labeled fields:\n"
                "- First Name / Given Name\n"
                "- Last Name / Surname\n"
                "- National ID / CNP\n"
                "- Job Title / Role\n"
                "- Department\n"
                "- Start Date / Effective Date\n"
                "- Reporting Manager ID\n"
                "- Employment Type (full-time, part-time, contractor)\n"
                "- Work Location (remote, hybrid, onsite)\n"
                "- Delivery / Residential Address\n"
                "- Contact Phone Number\n"
            )

        if doc_type == DocumentType.NATIONAL_ID:
            return base_instruction + (
                "Document Type: NATIONAL IDENTITY CARD / PASSPORT\n"
                "Extract:\n"
                "- First Name / Given Name\n"
                "- Last Name / Surname\n"
                "- National Identification Number (ID / SSN / Personal Number)\n"
            )

        if doc_type == DocumentType.MEDICAL_CLEARANCE:
            return base_instruction + (
                "Document Type: OCCUPATIONAL HEALTH / MEDICAL CLEARANCE CERTIFICATE\n"
                "Extract:\n"
                "- Medical Conclusion: check if marked with X as 'FIT FOR WORK'/'APT PENTRU MUNCA', or 'UNFIT FOR WORK'/'INAPT PENTRU MUNCA'\n"
                "- Examination Date / Issue Date\n"
            )

        return base_instruction + "Transcribe all visible information accurately."

    @classmethod
    def extract(
        cls,
        pages: list[DocumentPage],
        doc_type: DocumentType,
        model: Optional[str] = None,
    ) -> str:
        """
        Processes document pages through the local Ollama Vision LLM.
        Returns the model's visual analysis and transcription.
        """
        if not pages:
            return "[NO PAGES PROVIDED]"

        selected_model = model or OLLAMA_VISION_MODEL
        target_pages = pages[:MAX_VISION_PAGES]

        logger.info(f"\n--- 👁️ [TRACK B START] Model='{selected_model}' | DocType='{doc_type.value}' ---")
        logger.info(f"   └── Encoding {len(target_pages)} page image(s) to Base64...")

        # Convert target page images to base64
        images_b64 = [cls._image_to_base64(p.image) for p in target_pages]
        prompt = cls._build_vision_prompt(doc_type)

        logger.info(
            f"Track B: Sending {len(images_b64)} image(s) to Ollama ({selected_model}) "
            f"for doc_type='{doc_type.value}'."
        )

        start_time = time.time()
        try:
            response = ollama.chat(
                model=selected_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": images_b64,
                    }
                ],
                options={
                   "temperature": 0.1,         
                    "repeat_penalty": 1.3,      
                    "num_predict": 256,         
                    "stop": ["<|eot_id|>", "--- END ---"],
                },
            )
            elapsed = time.time() - start_time
            raw_text = response.get("message", {}).get("content", "").strip()

            logger.info(f"--- 👁️ [TRACK B COMPLETE] (Elapsed: {elapsed:.2f}s) ---")
            logger.info(f">>> RAW VISION TRANSCRIPTION:\n{raw_text}\n" + "-" * 50)
            return raw_text if raw_text else "[VISION MODEL RETURNED EMPTY RESPONSE]"
        except Exception as e:
            logger.error(f"Track B Vision extraction failed: {e}")
            return f"[VISION EXTRACTION ERROR: {str(e)}]"