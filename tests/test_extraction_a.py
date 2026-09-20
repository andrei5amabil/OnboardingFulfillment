import io
import sys
from pathlib import Path
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont

from src.extraction.preprocessing import DocumentPreprocessor
from src.extraction.parse_ocr import TrackAExtractor


def create_synthetic_digital_pdf() -> bytes:
    """Creates an in-memory PDF containing a rich digital text layer."""
    doc = fitz.open()
    page = doc.new_page()
    sample_text = (
        "CONTRACT INDIVIDUAL DE MUNCA\n"
        "Incheiat astazi 2026-09-01 intre angajator si angajat.\n"
        "Functia: Senior Backend Engineer\n"
        "Departament: Engineering\n"
        "Locatia: Timisoara, Romania\n"
        "Prezentul contract intra in vigoare la data mentionata."
    )
    # Insert text directly into the PDF text layer
    page.insert_text((50, 50), sample_text, fontsize=12)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def create_synthetic_scanned_image() -> bytes:
    """Creates an in-memory PNG image containing text (simulating an ID card / photo)."""
    # Create a 600x300 image
    img = Image.new("RGB", (600, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Draw text as pixels (no digital text layer)
    sample_text = (
        "ROMANIA - CARTE DE IDENTITATE\n"
        "NUME: POPESCU\n"
        "PRENUME: ANDREI\n"
        "CNP: 5050223350041"
    )
    draw.text((30, 40), sample_text, fill=(0, 0, 0))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def run_synthetic_tests():
    print("==================================================")
    print("RUNNING TRACK A SYNTHETIC TESTS")
    print("==================================================")

    # Test 1: Digital PDF (Should trigger digital extraction, bypass OCR)
    print("\n--- Test 1: Digital PDF Stream ---")
    digital_pdf_bytes = create_synthetic_digital_pdf()
    pages = DocumentPreprocessor.validate_and_load(
        file_bytes=digital_pdf_bytes,
        content_type="application/pdf",
        filename="contract_digital.pdf",
    )
    print(f"Loaded {len(pages)} page(s). Length of embedded text: {len(pages[0].text)}")

    output_text = TrackAExtractor.extract(pages, lang="eng+ron")
    print("\nResult Track A Output:")
    print(output_text)
    assert "CONTRACT INDIVIDUAL DE MUNCA" in output_text, "Failed to extract digital text!"
    print("✅ Test 1 Passed: Digital text extracted successfully without OCR fallback.")

    # Test 2: Image / Scanned Document (Must trigger OCR fallback)
    print("\n--- Test 2: Image Scan (OCR Fallback) ---")
    image_bytes = create_synthetic_scanned_image()
    pages = DocumentPreprocessor.validate_and_load(
        file_bytes=image_bytes,
        content_type="image/png",
        filename="buletin_scan.png",
    )
    print(f"Loaded {len(pages)} page(s). Length of embedded text: {len(pages[0].text)}")

    output_text = TrackAExtractor.extract(pages, lang="eng+ron")
    print("\nResult Track A Output:")
    print(output_text)
    assert "POPESCU" in output_text or "ROMANIA" in output_text, "Failed OCR extraction!"
    print("✅ Test 2 Passed: OCR fallback triggered and transcribed pixels successfully.")


def run_file_test(file_path_str: str):
    path = Path(file_path_str)
    if not path.exists():
        print(f"Error: File '{file_path_str}' not found.")
        sys.exit(1)

    print("==================================================")
    print(f"RUNNING TRACK A ON FILE: {path.name}")
    print("==================================================")

    file_bytes = path.read_bytes()
    pages = DocumentPreprocessor.validate_and_load(
        file_bytes=file_bytes,
        content_type=None,
        filename=path.name,
    )
    print(f"File parsed into {len(pages)} page(s).")

    output_text = TrackAExtractor.extract(pages, lang="eng+ron")
    print("\nResult Track A Output:")
    print(output_text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file_test(sys.argv[1])
    else:
        run_synthetic_tests()