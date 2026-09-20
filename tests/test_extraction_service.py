import io
import sys
from pathlib import Path

# Anchor project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PIL import Image, ImageDraw
from src.extraction.schemas import DocumentType
from src.extraction.service import DocumentExtractionService


def create_synthetic_id_card() -> bytes:
    """Creates a synthetic Romanian ID card image."""
    img = Image.new("RGB", (700, 350), color=(240, 245, 250))
    draw = ImageDraw.Draw(img)

    draw.text((40, 30), "ROMANIA - CARTE DE IDENTITATE", fill=(0, 0, 0))
    draw.text((40, 70), "SERIA RK NR 987654", fill=(0, 0, 0))
    draw.text((40, 110), "CNP 1980315123456", fill=(0, 0, 0))
    draw.text((40, 150), "Nume: IONESCU", fill=(0, 0, 0))
    draw.text((40, 190), "Prenume: RADU", fill=(0, 0, 0))
    draw.text((40, 230), "Cetatenie: Romana", fill=(0, 0, 0))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_full_pipeline_id():
    print("==================================================")
    print("RUNNING END-TO-END EXTRACTION SERVICE TEST")
    print("==================================================")

    id_bytes = create_synthetic_id_card()

    response = DocumentExtractionService.process_document(
        file_bytes=id_bytes,
        filename="buletin_radu.png",
        doc_type=DocumentType.NATIONAL_ID,
        content_type="image/png",
    )

    print("\n--- Complete Pipeline Response Envelope ---")
    print(response.model_dump_json(indent=2))
    print("--------------------------------------------")

    assert response.status == "success"
    assert response.data.last_name == "IONESCU"
    assert response.data.first_name == "RADU"
    assert response.data.national_id == "1980315123456"
    print("✅ Full extraction pipeline completed successfully!")


if __name__ == "__main__":
    test_full_pipeline_id()