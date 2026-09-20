import io
import sys
from pathlib import Path

# Anchor project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PIL import Image, ImageDraw
from src.extraction.preprocessing import DocumentPreprocessor
from src.extraction.schemas import DocumentType
from src.extraction.vllm_extract import TrackBExtractor


def create_synthetic_medical_certificate() -> bytes:
    """Generates an image simulating a stamped medical clearance certificate."""
    img = Image.new("RGB", (700, 400), color=(250, 250, 250))
    draw = ImageDraw.Draw(img)

    # Document Header
    draw.text((40, 30), "MEDICINA MUNCII - FISA DE APTITUDINE", fill=(0, 0, 0))
    draw.text((40, 60), "Data examinarii: 2026-08-25", fill=(0, 0, 0))
    draw.text((40, 90), "Salariat: Popescu Andrei", fill=(0, 0, 0))
    draw.text((40, 120), "Functia: Software Engineer", fill=(0, 0, 0))

    # Stamped decision simulation
    draw.rectangle([(40, 180), (320, 260)], outline=(180, 0, 0), width=3)
    draw.text((55, 195), "CONCLUZIE MEDICALA:", fill=(180, 0, 0))
    draw.text((55, 220), "[X] APT PENTRU MUNCA", fill=(180, 0, 0))

    # Stamp details
    draw.text((40, 310), "Dr. Ionescu Radu - Medic Primar", fill=(50, 50, 50))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def run_synthetic_vision_test():
    print("==================================================")
    print("RUNNING TRACK B SYNTHETIC TEST (Vision LLM)")
    print("==================================================")

    cert_bytes = create_synthetic_medical_certificate()
    pages = DocumentPreprocessor.validate_and_load(
        file_bytes=cert_bytes,
        content_type="image/png",
        filename="fisa_medicala.png",
    )
    print(f"Loaded {len(pages)} page(s) into DocumentPage structure.")

    output = TrackBExtractor.extract(
        pages=pages,
        doc_type=DocumentType.MEDICAL_CLEARANCE,
    )

    print("\n--- Track B Vision Model Output ---")
    print(output)
    print("-----------------------------------")


def run_file_vision_test(file_path_str: str, doc_type_str: str):
    path = Path(file_path_str)
    if not path.exists():
        print(f"Error: File '{file_path_str}' does not exist.")
        sys.exit(1)

    try:
        doc_type = DocumentType(doc_type_str)
    except ValueError:
        print(f"Invalid doc_type. Choose from: {[d.value for d in DocumentType]}")
        sys.exit(1)

    print("==================================================")
    print(f"RUNNING TRACK B ON: {path.name} ({doc_type.value})")
    print("==================================================")

    file_bytes = path.read_bytes()
    pages = DocumentPreprocessor.validate_and_load(
        file_bytes=file_bytes,
        content_type=None,
        filename=path.name,
    )

    output = TrackBExtractor.extract(pages=pages, doc_type=doc_type)
    print("\n--- Track B Vision Model Output ---")
    print(output)
    print("-----------------------------------")


if __name__ == "__main__":
    # Usage:
    # 1. python -m tests.test_track_b
    # 2. python -m tests.test_track_b /path/to/img.png medical_clearance
    if len(sys.argv) > 2:
        run_file_vision_test(sys.argv[1], sys.argv[2])
    else:
        run_synthetic_vision_test()