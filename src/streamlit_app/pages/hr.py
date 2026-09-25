import os
import requests
import streamlit as st
from datetime import date, datetime
from dotenv import load_dotenv
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.extraction.validation import validate_cross_documents

env_path = PROJECT_ROOT / ".env"

DEPARTMENTS = [
    "Software Engineering & Application Modernization",
    "Cloud Infrastructure & Platforms",
    "Cybersecurity & Digital Identity",
    "Data Analytics, AI & Business Intelligence",
    "Quality Assurance & Test Automation",
    "IT Service Management & Workplace Operations",
    "Digital Consulting & Transformation Advisory",
    "Product Management & UX/UI Design",
    "Enterprise Architecture & Solutions Design",
    "Human Resources & Talent Acquisition",
    "Finance, Legal & Corporate Governance",
    "Sales, Presales & Account Management",
    "Project Management Office (PMO)",
    "Internal IT & Information Security",
    "Marketing & Corporate Communications",
    "Procurement & Supply Chain Management",
]

DEPARTMENT_ROLE_MAPPING = {
    "Software Engineering & Application Modernization": [
        "Junior Frontend Developer", "Frontend Developer", "Senior Frontend Developer",
        "Junior Backend Engineer", "Backend Engineer", "Senior Backend Engineer",
        "Junior Full-Stack Engineer", "Full-Stack Engineer", "Senior Full-Stack Engineer",
        "Lead Software Engineer", "Software Architect",
    ],
    "Cloud Infrastructure & Platforms": [
        "Junior DevOps Engineer", "DevOps Engineer", "Senior DevOps Engineer",
        "Junior Cloud Engineer", "Cloud Solutions Architect", "Site Reliability Engineer (SRE)",
        "Systems Administrator",
    ],
    "Cybersecurity & Digital Identity": [
        "Junior Security Analyst", "SOC Analyst", "Cybersecurity Engineer",
        "Penetration Tester", "IAM Specialist", "GRC Consultant",
    ],
    "Data Analytics, AI & Business Intelligence": [
        "Junior Data Analyst", "Data Analyst", "Junior Data Engineer",
        "Data Engineer", "Senior Data Engineer", "Machine Learning Engineer",
        "AI/ML Research Scientist", "BI Developer",
    ],
    "Quality Assurance & Test Automation": [
        "Junior QA Tester", "QA Automation Engineer", "Senior QA Automation Engineer",
        "Performance Test Specialist", "Test Lead",
    ],
    "IT Service Management & Workplace Operations": [
        "IT Service Desk Specialist (L1/L2)", "Senior Service Desk Engineer (L3)",
        "Incident & Problem Manager", "Service Delivery Manager",
        "Workplace Support Technician", "IT Operations Lead",
    ],
    "Digital Consulting & Transformation Advisory": [
        "Associate Consultant", "Technology Consultant", "Senior Digital Consultant",
        "Consulting Manager", "Solutions Architect",
    ],
    "Product Management & UX/UI Design": [
        "Junior UI/UX Designer", "UI/UX Designer", "Senior Product Designer",
        "Product Owner", "Technical Product Manager",
    ],
    "Enterprise Architecture & Solutions Design": [
        "Associate Solutions Architect", "Enterprise Architect", "Chief Solutions Architect",
        "Domain Architect (Cloud/Data/Security)", "Integration Architect", "Technology Strategy Consultant",
    ],
    "Human Resources & Talent Acquisition": [
        "Talent Acquisition Specialist", "HR Operations Specialist", "HR Business Partner",
        "Learning & Development Specialist", "Compensation & Benefits Analyst",
    ],
    "Finance, Legal & Corporate Governance": [
        "Financial Analyst", "Senior Corporate Accountant", "Legal Counsel / Contract Specialist",
        "Compliance & Regulatory Officer", "Tax & Treasury Specialist", "Financial Controller",
    ],
    "Sales, Presales & Account Management": [
        "Business Development Representative (BDR)", "Account Executive", "Senior Key Account Manager",
        "Presales Solution Consultant", "Bid & Proposal Manager", "Sales Director",
    ],
    "Project Management Office (PMO)": [
        "PMO Analyst", "Scrum Master", "Junior Project Manager",
        "Project Manager", "Senior Project Manager", "Program Director",
    ],
    "Internal IT & Information Security": [
        "Internal Systems Administrator", "Network & Systems Engineer", "Internal IT Support Specialist",
        "Information Security Analyst", "Endpoint Management Specialist", "Internal IT Infrastructure Lead",
    ],
    "Marketing & Corporate Communications": [
        "Content Marketing Specialist", "Digital Marketing Manager", "Corporate Communications Specialist",
        "Brand & Public Relations Manager", "Event & Campaign Coordinator", "Internal Communications Officer",
    ],
    "Procurement & Supply Chain Management": [
        "Procurement Specialist", "IT Vendor Manager", "Sourcing & Contract Specialist",
        "Supply Chain Analyst", "Category Manager (Hardware & Software)", "Purchasing Officer",
    ],
}

LOCATION_OPTIONS = ["Romania, Timisoara", "France, Paris", "China, Beijing"]
WORK_LOCATION_OPTIONS = ["on-site", "remote", "hybrid"]
EMPLOYMENT_TYPE_OPTIONS = ["full-time", "part-time", "contract"]

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- Session State Initialization ---
if "user_id" not in st.session_state:
    st.session_state.user_id = "EMP-0042"

# Add to your session state initialization:
if "scanned_documents" not in st.session_state:
    st.session_state.scanned_documents = {
        "contract": {},
        "national_id": {},
        "medical_clearance": {},
    }
if "validation_alerts" not in st.session_state:
    st.session_state.validation_alerts = []

form_fields = {
    "first_name": "",
    "last_name": "",
    "national_id": "",
    "department": DEPARTMENTS[0],
    "role": DEPARTMENT_ROLE_MAPPING[DEPARTMENTS[0]][0],
    "location": LOCATION_OPTIONS[0],
    "work_location": WORK_LOCATION_OPTIONS[0],
    "start_date": date.today(),
    "employment_type": EMPLOYMENT_TYPE_OPTIONS[0],
    "manager_id": "",
    "shipping_address": "",
    "contact_phone": "",
    "medical_clearance_status": False,
    "medical_clearance_date": date.today(),
    "notes": "",
    "is_scanning": False,
    "extraction_alerts": [],
}

for key, default in form_fields.items():
    if key not in st.session_state:
        st.session_state[key] = default

def format_name(name: str | None) -> str:
    """
    Normalizes capitalization for personal names.
    Handles all-caps, all-lowercase, hyphens, apostrophes, and diacritics.
    
    Examples:
        'JOHN DOE'       -> 'John Doe'
        'jean-luc'       -> 'Jean-Luc'
        'O\'CONNOR'      -> 'O\'Connor'
        'mcdonald'       -> 'McDonald'
        'șerban popescu' -> 'Șerban Popescu'
    """
    if not name or not isinstance(name, str):
        return ""

    def _capitalize_part(part: str) -> str:
        if not part:
            return ""
        # Handle Celtic 'Mc' prefix (e.g., McDonald)
        if part.lower().startswith("mc") and len(part) > 2:
            return "Mc" + part[2:].capitalize()
        return part.capitalize()

    def _capitalize_token(token: str) -> str:
        # Split on apostrophes (e.g., O'Connor, D'Angelo)
        apostrophe_parts = token.split("'")
        return "'".join(_capitalize_part(p) for p in apostrophe_parts)

    words = name.strip().split()
    formatted_words = []

    for word in words:
        # Split on hyphens (e.g., Anne-Marie)
        hyphen_parts = word.split("-")
        formatted_words.append("-".join(_capitalize_token(p) for p in hyphen_parts))

    return " ".join(formatted_words)

def parse_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return date.today()


def match_option(value: str | None, options: list[str], default: str) -> str:
    """Robust substring/case-insensitive matcher that falls back to existing value if unmatched."""
    if not value or not value.strip():
        return default
    val_clean = value.strip().lower()
    for opt in options:
        if val_clean in opt.lower() or opt.lower() in val_clean:
            return opt
    return default


def process_single_document(uploaded_file, document_type: str) -> bool:
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        data = {"document_type": document_type}
        res = requests.post(f"{API_URL}/onboarding/extract-document", files=files, data=data, timeout=90)

        if res.status_code == 200:
            payload = res.json()
            extracted = payload.get("data", {})
            flags = payload.get("confidence_flags", [])
            st.session_state.scanned_documents[document_type] = extracted

            # Re-run cross-validation across all scanned documents so far
            st.session_state.validation_alerts = validate_cross_documents(
                contract_data=st.session_state.scanned_documents.get("contract", {}),
                national_id_data=st.session_state.scanned_documents.get("national_id", {}),
                medical_data=st.session_state.scanned_documents.get("medical_clearance", {}),
            )
            if document_type == "contract":
                if extracted.get("department"):
                    st.session_state.department = match_option(
                        extracted["department"], DEPARTMENTS, st.session_state.department
                    )
                available_roles = DEPARTMENT_ROLE_MAPPING.get(st.session_state.department, [])
                if extracted.get("role"):
                    st.session_state.role = match_option(
                        extracted["role"], available_roles, st.session_state.role
                    )
                if extracted.get("start_date"):
                    st.session_state.start_date = parse_date(extracted["start_date"])
                if extracted.get("manager_id"):
                    st.session_state.manager_id = extracted["manager_id"]
                if extracted.get("shipping_address"):
                    st.session_state.shipping_address = extracted["shipping_address"]
                if extracted.get("contact_phone"):
                    st.session_state.contact_phone = extracted["contact_phone"]
                if extracted.get("work_location"):
                    st.session_state.work_location = match_option(
                        extracted["work_location"].replace("_", "-"),
                        WORK_LOCATION_OPTIONS,
                        st.session_state.work_location,
                    )
                if extracted.get("employment_type"):
                    st.session_state.employment_type = match_option(
                        extracted["employment_type"].replace("_", "-"),
                        EMPLOYMENT_TYPE_OPTIONS,
                        st.session_state.employment_type,
                    )

            elif document_type == "national_id":
                if extracted.get("first_name"):
                    st.session_state.first_name = format_name(extracted["first_name"])
                if extracted.get("last_name"):
                    st.session_state.last_name = format_name(extracted["last_name"])
                if extracted.get("national_id"):
                    st.session_state.national_id = extracted["national_id"]

            elif document_type == "medical_clearance":
                st.session_state.medical_clearance_status = bool(
                    extracted.get("medical_clearance_status", False)
                )
                if extracted.get("issue_date"):
                    st.session_state.medical_clearance_date = parse_date(extracted["issue_date"])

            st.session_state.extraction_alerts.extend(flags)
            return True
        else:
            st.error(f"Failed to extract {uploaded_file.name}: {res.text}")
            return False
    except Exception as e:
        st.error(f"Error processing {uploaded_file.name}: {e}")
        return False


def run_batch_extraction(doc_queue: list[tuple]):
    st.session_state.is_scanning = True
    st.session_state.extraction_alerts = []
    with st.status(f"Processing {len(doc_queue)} document(s)...", expanded=True) as status:
        for file_obj, doc_type in doc_queue:
            status.write(f"Scanning **{file_obj.name}** ({doc_type})...")
            process_single_document(file_obj, doc_type)
        status.update(label="All documents processed!", state="complete", expanded=False)
    st.session_state.is_scanning = False
    st.rerun()


# --- Streamlit Layout ---
st.title("📝 Assisted Employee Onboarding Intake")
st.caption("Upload candidate documents to pre-fill identity, contract, logistics, and compliance data.")

# --- Document Dropzones ---
st.subheader("1. Document Ingestion Dropzones")

doc_col1, doc_col2, doc_col3 = st.columns(3)

with doc_col1:
    st.markdown("**📄 Employment Contract**")
    f_contract = st.file_uploader(
        "Contract (PDF/Image)",
        type=["pdf", "png", "jpg", "jpeg"],
        key="uploader_contract",
        disabled=st.session_state.is_scanning,
    )
    scan_contract_btn = st.button(
        "Scan Contract",
        use_container_width=True,
        disabled=st.session_state.is_scanning or not f_contract,
    )

with doc_col2:
    st.markdown("**🪪 National Photo ID**")
    f_id = st.file_uploader(
        "ID Card (PDF/Image)",
        type=["pdf", "png", "jpg", "jpeg"],
        key="uploader_id",
        disabled=st.session_state.is_scanning,
    )
    scan_id_btn = st.button(
        "Scan ID Card",
        use_container_width=True,
        disabled=st.session_state.is_scanning or not f_id,
    )

with doc_col3:
    st.markdown("**🏥 Medical Clearance**")
    f_med = st.file_uploader(
        "Medical Certificate (PDF/Image)",
        type=["pdf", "png", "jpg", "jpeg"],
        key="uploader_med",
        disabled=st.session_state.is_scanning,
    )
    scan_med_btn = st.button(
        "Scan Medical",
        use_container_width=True,
        disabled=st.session_state.is_scanning or not f_med,
    )

# Master Ingestion Button
available_uploads = []
if f_contract: available_uploads.append((f_contract, "contract"))
if f_id: available_uploads.append((f_id, "national_id"))
if f_med: available_uploads.append((f_med, "medical_clearance"))

scan_all_btn = st.button(
    f"Scan All Uploaded Documents ({len(available_uploads)} ready)",
    type="secondary",
    use_container_width=True,
    disabled=st.session_state.is_scanning or len(available_uploads) == 0,
)

if scan_all_btn:
    run_batch_extraction(available_uploads)
elif scan_contract_btn:
    run_batch_extraction([(f_contract, "contract")])
elif scan_id_btn:
    run_batch_extraction([(f_id, "national_id")])
elif scan_med_btn:
    run_batch_extraction([(f_med, "medical_clearance")])

if st.session_state.extraction_alerts:
    for alert in st.session_state.extraction_alerts:
        st.warning(alert)

# --- Render Cross-Document Validation Alerts ---
if st.session_state.validation_alerts:
    for alert in st.session_state.validation_alerts:
        if alert.severity == "critical":
            st.error(f"🚨 **{alert.field.upper()}**: {alert.message}")
        elif alert.severity == "warning":
            st.warning(f"⚠️ **{alert.field.upper()}**: {alert.message}")
        else:
            st.info(f"ℹ️ **{alert.field.upper()}**: {alert.message}")

st.subheader("2. Candidate Profile & Review")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 👤 Identity & Role")
    first_name = st.text_input("First Name", value=st.session_state.first_name)
    last_name = st.text_input("Last Name", value=st.session_state.last_name)
    national_id = st.text_input("National ID / CNP", value=st.session_state.national_id)

    dept_idx = DEPARTMENTS.index(st.session_state.department) if st.session_state.department in DEPARTMENTS else 0
    department = st.selectbox("Department", options=DEPARTMENTS, index=dept_idx)

    available_roles = DEPARTMENT_ROLE_MAPPING.get(department, [])
    role_idx = available_roles.index(st.session_state.role) if st.session_state.role in available_roles else 0
    role = st.selectbox("Role", options=available_roles, index=role_idx)

    manager_id = st.text_input("Manager ID (Optional)", value=st.session_state.manager_id)
    start_date = st.date_input("Start Date", value=st.session_state.start_date)

    emp_type_idx = (
        EMPLOYMENT_TYPE_OPTIONS.index(st.session_state.employment_type)
        if st.session_state.employment_type in EMPLOYMENT_TYPE_OPTIONS
        else 0
    )
    employment_type = st.selectbox("Employment Type", options=EMPLOYMENT_TYPE_OPTIONS, index=emp_type_idx)

with col2:
    st.markdown("##### 🚚 Logistics & Compliance")
    loc_idx = LOCATION_OPTIONS.index(st.session_state.location) if st.session_state.location in LOCATION_OPTIONS else 0
    location = st.selectbox("Office Location", options=LOCATION_OPTIONS, index=loc_idx)

    work_loc_idx = (
        WORK_LOCATION_OPTIONS.index(st.session_state.work_location)
        if st.session_state.work_location in WORK_LOCATION_OPTIONS
        else 0
    )
    work_location = st.selectbox("Work Location", options=WORK_LOCATION_OPTIONS, index=work_loc_idx)

    shipping_address = st.text_area("Delivery Address (Required for Remote/Hybrid)", value=st.session_state.shipping_address, height=85)
    contact_phone = st.text_input("Contact Phone Number", value=st.session_state.contact_phone)

    st.markdown("##### 🏥 Medical Gatekeeper")
    med_status = st.checkbox(
        "Medical Clearance Confirmed (Fit for Work)",
        value=st.session_state.medical_clearance_status,
    )
    med_date = st.date_input("Clearance Examination Date", value=st.session_state.medical_clearance_date)

notes = st.text_area("Additional Onboarding Notes (Special Software/Hardware Requests)", value=st.session_state.notes)

# Submission
if st.button("Initiate Onboarding", type="primary", use_container_width=True):
    if not all((first_name.strip(), last_name.strip(), department, role, start_date, employment_type)):
        st.error("Please fill in all required identity and job role fields.")
    else:
        discrepancy_notes = [
            f"[{a.severity.upper()}] {a.message}"
            for a in st.session_state.validation_alerts
            if a.severity == "critical"
        ]

        clean_first_name = format_name(first_name)
        clean_last_name = format_name(last_name)

        final_notes = notes.strip()
        if discrepancy_notes:
            final_notes += "\n\n### AUTOMATED DOCUMENT DISCREPANCY FLAGS:\n" + "\n".join(discrepancy_notes)
        payload = {
            "first_name": clean_first_name.strip(),
            "last_name": clean_last_name.strip(),
            "national_id": national_id.strip() if national_id else None,
            "department": department,
            "role": role,
            "manager_id": manager_id.strip() if manager_id else None,
            "start_date": str(start_date),
            "employment_type": employment_type,
            "location": location,
            "work_location": work_location,
            "shipping_address": shipping_address.strip() if shipping_address else None,
            "contact_phone": contact_phone.strip() if contact_phone else None,
            "medical_clearance_status": med_status,
            "medical_clearance_date": str(med_date) if med_status else None,
            "hr_manager_id": st.session_state.user_id,
            "notes": final_notes,
        }

        try:
            res = requests.post(f"{API_URL}/onboarding/requests", json=payload, timeout=15)
            if res.status_code == 200:
                st.success(f"Onboarding request created for **{first_name} {last_name}**!")
                st.json(res.json())
            else:
                st.error(f"Failed to submit: {res.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not reach backend service.")