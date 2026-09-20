import base64
import io
import logging
import os
from typing import Optional
import ollama
from PIL import Image

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
            "Extract all relevant entities, transcribed text, and visual markers. "
            "Be concise, precise with spelling, and extract each piece of information ONCE. "
            "Consider both English and Romanian text."
            "Do NOT repeat the extracted text or loop. Stop when complete.\n\n"
        )

        if doc_type == DocumentType.CONTRACT:
            return base_instruction + (
                "Document Type: EMPLOYMENT CONTRACT\n"
                "Focus specifically on:\n"
                "- Job Title / Role\n"
                "- Department\n"
                "- Contract Start Date / Effective Date\n"
                "- Manager or Supervisor reference\n"
                "- Employment Type (full-time, part-time, contractor)\n"
                "- Work Location (remote, hybrid, onsite, city)\n"
                "Transcribe any labeled values clearly."
            )

        if doc_type == DocumentType.NATIONAL_ID:
            return base_instruction + (
                "Document Type: NATIONAL IDENTITY CARD / PASSPORT\n"
                "Focus specifically on:\n"
                "- Last Name / Surname (Nume)\n"
                "- First Name / Given Name (Prenume)\n"
                "- National Identification Number (CNP / Personal ID Number / Passport No)\n"
                "Make sure not to confuse labels with the actual names."
            )

        if doc_type == DocumentType.HARDWARE_DELIVERY:
            return base_instruction + (
                "Document Type: HARDWARE DELIVERY / LOGISTICS FORM\n"
                "Focus specifically on:\n"
                "- Full Recipient Delivery / Shipping Address (Street, City, Postal Code)\n"
                "- Contact Phone Number for courier\n"
                "- Any recipient special delivery notes"
            )

        if doc_type == DocumentType.MEDICAL_CLEARANCE:
            return base_instruction + (
                "Document Type: MEDICAL CLEARANCE / OCCUPATIONAL HEALTH CERTIFICATE (Fisa de Aptitudine)\n"
                "Focus specifically on:\n"
                "- Clearance Verdict / Status: Look for stamps, checks, or text indicating 'APT' (Fit for work) "
                "or 'INAPT' (Unfit for work).\n"
                "- Date of medical examination / Issue date.\n"
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

        # Convert target page images to base64
        images_b64 = [cls._image_to_base64(p.image) for p in target_pages]
        prompt = cls._build_vision_prompt(doc_type)

        logger.info(
            f"Track B: Sending {len(images_b64)} image(s) to Ollama ({selected_model}) "
            f"for doc_type='{doc_type.value}'."
        )

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
                    "repeat_penalty": 1.2,      
                    "num_predict": 512,         
                    "stop": ["<|eot_id|>", "--- END ---"],
                },
            )
            raw_text = response.get("message", {}).get("content", "").strip()
            return raw_text if raw_text else "[VISION MODEL RETURNED EMPTY RESPONSE]"
        except Exception as e:
            logger.error(f"Track B Vision extraction failed: {e}")
            return f"[VISION EXTRACTION ERROR: {str(e)}]"