import sys
from pathlib import Path

# Anchor project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.extraction.schemas import DocumentType
from src.extraction.llm_formatter import TrackCJudge


def test_medical_clearance_arbitration():
    print("==================================================")
    print("RUNNING TRACK C ARBITRATION TEST (Medical Clearance)")
    print("==================================================")

    # Simulated output from Track A (OCR)
    track_a_sample = """
    MEDICINA MUNCII - FISA DE APTITUDINE
    Data examinarii: 2026-08-25
    Salariat: Popescu Andrei
    Functia: Software Engineer
    CONCLUZIE MEDICALA:
    APT PENTRU MUNCA
    Dr. Ionescu Radu
    """

    # Real noisy output captured from your Track B run
    track_b_sample = """
    The extracted text includes:
    - MEDICINA MUNCI - FISA DE APTITUDINE
    - Data examinari: 2026-08-25
    - Salariat Popescu Andrei
    - Functia: Software Engineer
    - CONCLUIZIE MEDICALA [Å PTFENTRU MUNCA] (conclusion medical for occupation)
    - Dr. ionescu Radu - Medic Primar
    """

    result = TrackCJudge.arbitrate(
        doc_type=DocumentType.MEDICAL_CLEARANCE,
        track_a_text=track_a_sample,
        track_b_text=track_b_sample,
    )

    print("\n--- Track C Validated Pydantic Result ---")
    print(f"Type: {type(result)}")
    print(f"Data: {result.model_dump_json(indent=2)}")
    print("-----------------------------------------")

    assert result.medical_clearance_status is True, "Expected status to resolve to True!"
    assert str(result.issue_date) == "2026-08-25", "Expected issue_date to match '2026-08-25'!"
    print("✅ Medical Clearance arbitration passed successfully!")


def test_national_id_arbitration():
    print("\n==================================================")
    print("RUNNING TRACK C ARBITRATION TEST (National ID)")
    print("==================================================")

    track_a_sample = """
    ROMANIA
    CARTE DE IDENTITATE
    SERIA RK NR 123456
    CNP 1980101123456
    Nume POPESCU
    Prenume ANDREI
    Cetatenie Romana
    """

    track_b_sample = """
    ID Card Details:
    - Last Name: POPESCU
    - First Name: ANDREI
    - ID Number: 1980101123456
    - Document: Carte de Identitate
    """

    result = TrackCJudge.arbitrate(
        doc_type=DocumentType.NATIONAL_ID,
        track_a_text=track_a_sample,
        track_b_text=track_b_sample,
    )

    print("\n--- Track C Validated Pydantic Result ---")
    print(f"Type: {type(result)}")
    print(f"Data: {result.model_dump_json(indent=2)}")
    print("-----------------------------------------")

    assert result.first_name.upper() == "ANDREI"
    assert result.last_name.upper() == "POPESCU"
    assert result.national_id == "1980101123456"
    print("✅ National ID arbitration passed successfully!")


if __name__ == "__main__":
    test_medical_clearance_arbitration()
    test_national_id_arbitration()