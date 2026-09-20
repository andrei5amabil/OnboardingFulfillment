import io
from dataclasses import dataclass
from typing import Optional
import pymupdf as fitz 
from PIL import Image

ALLOWED_TYPES = {
    "application/pdf": "pdf",
    "image/jpeg": "jpeg",
    "image/png": "png",
    "image/webp": "webp",
}

MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB limit

@dataclass
class DocumentPage:
    page_number: int
    text: str              
    image: Image.Image     


class DocumentPreprocessor:

    @staticmethod
    def validate_and_load(file_bytes: bytes, content_type: Optional[str], filename: str) -> list[DocumentPage]:
        """
        Validates the incoming byte stream and standardizes both PDFs
        and standard image formats into a list of DocumentPage objects.
        """
        if len(file_bytes) == 0:
            raise ValueError("Uploaded file is empty.")

        if len(file_bytes) > MAX_FILE_SIZE_BYTES:
            raise ValueError(f"File size exceeds maximum limit of {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB.")

        # Determine format from MIME type or fallback to file extension
        ext = None
        if content_type in ALLOWED_TYPES:
            ext = ALLOWED_TYPES[content_type]
        else:
            lower_name = filename.lower()
            for allowed_ext in ["pdf", "jpeg", "jpg", "png", "webp"]:
                if lower_name.endswith(f".{allowed_ext}"):
                    ext = "jpeg" if allowed_ext == "jpg" else allowed_ext
                    break

        if not ext:
            raise ValueError(
                f"Unsupported file format for '{filename}'. Allowed formats: PDF, JPEG, PNG, WEBP."
            )

        if ext in ["jpeg", "png", "webp"]:
            try:
                pil_image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
                return [
                    DocumentPage(
                        page_number=1,
                        text="",
                        image=pil_image,
                    )
                ]
            except Exception as e:
                raise ValueError(f"Failed to decode image file: {str(e)}")

        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            pages = []
            for idx, page in enumerate(doc):
                embedded_text = page.get_text().strip()
                # Render page at 200 DPI for Vision / OCR consumption
                pix = page.get_pixmap(dpi=200)
                page_img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")

                pages.append(
                    DocumentPage(
                        page_number=idx + 1,
                        text=embedded_text,
                        image=page_img,
                    )
                )
            return pages
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {str(e)}")