import logging
from typing import Optional
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

from src.extraction.preprocessing import DocumentPage

logger = logging.getLogger("uvicorn.error")

# Minimum characters required to consider digital text valid
MIN_DIGITAL_TEXT_CHARS = 50


class TrackAExtractor:

    @staticmethod
    def preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
        """
        Applies grayscale, contrast boost, and slight sharpening
        to maximize Tesseract accuracy on smartphone photos and low-contrast scans.
        """
        # 1. Convert to grayscale
        gray = image.convert("L")

        # 2. Increase contrast
        enhancer = ImageEnhance.Contrast(gray)
        high_contrast = enhancer.enhance(1.8)

        # 3. Apply subtle sharpening filter
        sharpened = high_contrast.filter(ImageFilter.SHARPEN)
        return sharpened

    @classmethod
    def extract_page_text(cls, page: DocumentPage, lang: str = "ron+eng") -> str:
        """
        Extracts text from a single DocumentPage using digital text if present,
        or falls back to OCR if the page is an image or scanned.
        """
        embedded_text = page.text.strip()

        # Path 1: High-confidence digital text layer exists
        if len(embedded_text) >= MIN_DIGITAL_TEXT_CHARS:
            logger.info(f"   └── [Track A] Page {page.page_number}: Using native PDF text layer ({len(embedded_text)} chars)")
            return embedded_text

        # Path 2: Scanned PDF or raw photo upload -> Run OCR
        logger.info(f"   └── [Track A] Page {page.page_number}: Text layer missing/low ({len(embedded_text)} chars). Executing Tesseract OCR...")
        try:
            processed_img = cls.preprocess_image_for_ocr(page.image)
            # PSM 3 (Fully automatic page segmentation) is standard for forms/contracts
            ocr_config = "--oem 3 --psm 3"
            ocr_text = pytesseract.image_to_string(processed_img, lang=lang, config=ocr_config).strip()
            logger.info(f"       [Track A] OCR completed: {len(ocr_text)} chars extracted.")
            return ocr_text
        except Exception as e:
            logger.error(f"       [Track A] ❌ OCR failed on page {page.page_number}: {e}")
            # Fallback to whatever embedded text existed, even if sparse
            return embedded_text

    @classmethod
    def extract(cls, pages: list[DocumentPage], lang: str = "ron+eng") -> str:
        """
        Processes all pages in the document and returns a formatted text stream.
        """
        extracted_sections = []
        logger.info(f"\n--- 🔍 [TRACK A START] Processing {len(pages)} page(s) via Text/OCR ---")
        for page in pages:
            page_text = cls.extract_page_text(page, lang=lang)
            extracted_sections.append(
                f"--- [Page {page.page_number}] ---\n{page_text if page_text else '[NO TEXT DETECTED]'}"
            )
        full_output = "\n\n".join(extracted_sections)
        preview = full_output[:250].replace('\n', ' ')
        logger.info(f"--- 🔍 [TRACK A COMPLETE] Total Chars: {len(full_output)} | Preview: \"{preview}...\" ---\n")
        return full_output