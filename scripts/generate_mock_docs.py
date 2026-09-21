import argparse
import random
from datetime import date, timedelta
from pathlib import Path

import pymupdf as fitz 
from PIL import Image, ImageDraw

FIRST_NAMES_MALE = ["Andrei", "Alexandru", "Mihai", "Cristian", "Radu", "Stefan", "Vlad", "Ionut"]
FIRST_NAMES_FEMALE = ["Elena", "Ioana", "Andreea", "Maria", "Diana", "Roxana", "Ana", "Laura"]
LAST_NAMES = ["Popescu", "Ionescu", "Radu", "Dumitrescu", "Stan", "Gheorghe", "Stoica", "Nistor"]

DEPARTMENTS = [
    "Software Engineering & Application Modernization",
    "Cloud Infrastructure & Platforms",
    "Cybersecurity & Digital Identity",
    "Data Analytics, AI & Business Intelligence",
    "Quality Assurance & Test Automation",
    "IT Service Management & Workplace Operations",
    "Product Management & UX/UI Design",
    "Finance, Legal & Corporate Governance",
]

DEPARTMENT_ROLE_MAPPING = {
    "Software Engineering & Application Modernization": [
        "Junior Backend Engineer", "Backend Engineer", "Senior Backend Engineer",
        "Frontend Developer", "Senior Full-Stack Engineer", "Lead Software Engineer"
    ],
    "Cloud Infrastructure & Platforms": [
        "DevOps Engineer", "Senior Cloud Engineer", "Site Reliability Engineer (SRE)"
    ],
    "Cybersecurity & Digital Identity": [
        "SOC Analyst", "Cybersecurity Engineer", "IAM Specialist"
    ],
    "Data Analytics, AI & Business Intelligence": [
        "Data Analyst", "Senior Data Engineer", "Machine Learning Engineer"
    ],
    "Quality Assurance & Test Automation": [
        "QA Automation Engineer", "Senior QA Automation Engineer"
    ],
    "IT Service Management & Workplace Operations": [
        "IT Service Desk Specialist (L1/L2)", "Workplace Support Technician"
    ],
    "Product Management & UX/UI Design": [
        "UI/UX Designer", "Product Owner"
    ],
    "Finance, Legal & Corporate Governance": [
        "Financial Analyst", "Senior Corporate Accountant"
    ],
}

STREETS = ["Main Street", "King's Road", "Commercial Boulevard", "Innovation Way"]
CITIES = ["Timisoara", "London", "Dublin", "Amsterdam"]


def generate_candidate_persona(force_medically_unfit: bool = False):
    is_male = random.choice([True, False])
    first_name = random.choice(FIRST_NAMES_MALE if is_male else FIRST_NAMES_FEMALE)
    last_name = random.choice(LAST_NAMES)

    prefix = "5" if is_male else "6"
    year = f"{random.randint(0, 5):02d}"
    month = f"{random.randint(1, 12):02d}"
    day = f"{random.randint(1, 28):02d}"
    county = f"{random.randint(1, 40):02d}"
    seq = f"{random.randint(100, 999):03d}"
    first_12 = f"{prefix}{year}{month}{day}{county}{seq}"
    CONTROL_KEY = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    checksum = sum(int(d) * k for d, k in zip(first_12, CONTROL_KEY)) % 11
    control = 1 if checksum == 10 else checksum
    cnp = f"{first_12}{control}"
    
    department = random.choice(DEPARTMENTS)
    role = random.choice(DEPARTMENT_ROLE_MAPPING[department])
    shipping_address = f"{random.randint(10, 250)} {random.choice(STREETS)}, Suite {random.randint(1, 40)}, {random.choice(CITIES)}"
    phone = f"+40 7{random.randint(20, 79)} {random.randint(100, 999)} {random.randint(100, 999)}"

    start_date = (date.today() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d")
    med_exam_date = (date.today() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")

    return {
        "first_name": first_name,
        "last_name": last_name,
        "cnp": cnp,
        "department": department,
        "role": role,
        "manager_id": f"MGR-{random.randint(100, 999)}",
        "start_date": start_date,
        "work_location": random.choice(["remote", "hybrid", "on-site"]),
        "employment_type": "full_time",
        "shipping_address": shipping_address,
        "phone": phone,
        "med_exam_date": med_exam_date,
        "medical_status_apt": not force_medically_unfit,
    }


def create_contract_pdf(c: dict, output_path: Path):
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)

    text = f"""
                        EMPLOYMENT AGREEMENT
                        Contract ID: AGR-{random.randint(1000, 9999)} / Date: {date.today().strftime('%Y-%m-%d')}

1. THE PARTIES
Employer: ATOS SOFTWARE LTD
Employee: {c['first_name']} {c['last_name']}
National ID / CNP: {c['cnp']}
Delivery / Residential Address: {c['shipping_address']}
Contact Phone Number: {c['phone']}

2. APPOINTMENT & TERM
Job Title / Role: {c['role']}
Department: {c['department']}
Reporting Manager ID: {c['manager_id']}
Start Date / Effective Date: {c['start_date']}
Employment Type: {c['employment_type']}
Work Location: {c['work_location'].upper()} (Location: Romania, Timisoara)

3. LOGISTICS & HARDWARE ALLOCATION
The employee requires equipment provisioning dispatched to the registered delivery address above.

Authorized Signatory:                                         Employee Signature:
Director of HR                                                {c['first_name']} {c['last_name']}
    """
    page.insert_text((40, 50), text, fontsize=9.5, fontname="helv")
    doc.save(str(output_path))
    doc.close()


def create_national_id_image(c: dict, output_path: Path):
    img = Image.new("RGB", (850, 520), color=(235, 245, 252))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(10, 10), (840, 510)], outline=(100, 140, 180), width=3)
    draw.rectangle([(15, 15), (835, 75)], fill=(210, 230, 245))
    draw.text((30, 25), "IDENTITY CARD / CARTE DE IDENTITATE", fill=(20, 50, 100))
    draw.text((650, 35), f"SERIES ID  NR {random.randint(100000, 999999)}", fill=(0, 0, 0))

    draw.rectangle([(40, 100), (240, 360)], fill=(200, 210, 220), outline=(150, 160, 170), width=2)
    draw.text((100, 220), "[ PHOTO ]", fill=(120, 130, 140))

    fields = [
        ("National ID / CNP", c['cnp']),
        ("Surname / Last Name", c['last_name'].upper()),
        ("Given Names / First Name", c['first_name'].upper()),
        ("Nationality", "Romanian"),
        ("Address", c['shipping_address']),
    ]

    y = 110
    for label, val in fields:
        draw.text((270, y), label, fill=(110, 120, 130))
        draw.text((270, y + 18), val, fill=(0, 0, 0))
        y += 48

    draw.rectangle([(20, 420), (830, 495)], fill=(245, 248, 252))
    draw.text((40, 430), f"ID{c['last_name'].upper()}<<{c['first_name'].upper()}<<<<<<<<<<<<<<<<<<<<<<<<", fill=(50, 50, 50))
    draw.text((40, 460), f"{c['cnp']}0ROU<<<<<<<<<<<<<<<<<<<<6", fill=(50, 50, 50))
    img.save(str(output_path), format="PNG")


def create_medical_clearance_image(c: dict, output_path: Path):
    img = Image.new("RGB", (750, 550), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.text((40, 30), "OCCUPATIONAL HEALTH - MEDICAL CLEARANCE CERTIFICATE", fill=(0, 0, 0))
    draw.line([(40, 70), (710, 70)], fill=(180, 180, 180), width=2)

    draw.text((40, 90), f"Examination / Issue Date: {c['med_exam_date']}", fill=(0, 0, 0))
    draw.text((40, 120), f"Employee Full Name: {c['last_name'].upper()} {c['first_name'].upper()}", fill=(0, 0, 0))
    draw.text((40, 150), f"National ID / CNP: {c['cnp']}", fill=(0, 0, 0))
    draw.text((40, 180), f"Job Title / Role: {c['role']}", fill=(0, 0, 0))
    draw.text((40, 210), f"Department: {c['department']}", fill=(0, 0, 0))

    draw.rectangle([(40, 270), (450, 360)], outline=(0, 0, 0), width=2)
    draw.text((55, 285), "MEDICAL CONCLUSION:", fill=(0, 0, 0))

    apt_text = "[ X ] FIT FOR WORK / CLEARED" if c['medical_status_apt'] else "[   ] FIT FOR WORK / CLEARED"
    inapt_text = "[   ] UNFIT FOR WORK" if c['medical_status_apt'] else "[ X ] UNFIT FOR WORK"

    draw.text((65, 310), apt_text, fill=(0, 120, 0) if c['medical_status_apt'] else (100, 100, 100))
    draw.text((65, 330), inapt_text, fill=(180, 0, 0) if not c['medical_status_apt'] else (100, 100, 100))

    draw.ellipse([(520, 340), (680, 500)], outline=(200, 30, 30), width=3)
    draw.text((545, 390), "DR. RADU IONESCU", fill=(200, 30, 30))
    draw.text((540, 415), "OCCUPATIONAL MD", fill=(200, 30, 30))
    draw.text((560, 440), "ID 459812", fill=(200, 30, 30))
    img.save(str(output_path), format="PNG")


def generate_document_packet(output_dir: Path, force_unfit: bool = False):
    persona = generate_candidate_persona(force_medically_unfit=force_unfit)
    slug = f"{persona['first_name'].lower()}_{persona['last_name'].lower()}"
    target_dir = output_dir / f"candidate_{slug}"
    target_dir.mkdir(parents=True, exist_ok=True)

    contract_path = target_dir / "1_contract.pdf"
    id_path = target_dir / "2_national_id.png"
    medical_path = target_dir / "3_medical_clearance.png"

    create_contract_pdf(persona, contract_path)
    create_national_id_image(persona, id_path)
    create_medical_clearance_image(persona, medical_path)

    print(f"Generated 3-document packet for: {persona['first_name']} {persona['last_name']} ({persona['role']})")
    print(f"  📂 Folder: {target_dir.name}")


def main():
    parser = argparse.ArgumentParser(description="Generate mock onboarding document packets.")
    parser.add_argument("--count", type=int, default=1, help="Number of candidate packets to generate.")
    parser.add_argument("--out", type=str, default="mock_documents", help="Output directory.")
    parser.add_argument("--unfit", action="store_true", help="Generate an unfit medical certificate.")

    args = parser.parse_args()
    out_dir = Path(args.out).resolve()

    for _ in range(args.count):
        generate_document_packet(out_dir, force_unfit=args.unfit)

    print("✅ Document generation complete!")


if __name__ == "__main__":
    main()