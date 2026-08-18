import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DEPARTMENTS = [
    # Technology & Delivery Units
    "Software Engineering & Application Modernization",
    "Cloud Infrastructure & Platforms",
    "Cybersecurity & Digital Identity",
    "Data Analytics, AI & Business Intelligence",
    "Quality Assurance & Test Automation",
    "IT Service Management & Workplace Operations",
    "Digital Consulting & Transformation Advisory",
    "Product Management & UX/UI Design",
    "Enterprise Architecture & Solutions Design",
    # Corporate & Enabling Functions
    "Human Resources & Talent Acquisition",
    "Finance, Legal & Corporate Governance",
    "Sales, Presales & Account Management",
    "Project Management Office (PMO)",
    "Internal IT & Information Security",
    "Marketing & Corporate Communications",
    "Procurement & Supply Chain Management",
]
DEPARTMENT_ROLE_MAPPING = {
    # ---------------------------------------------------------
    # Technology & Delivery Units
    # ---------------------------------------------------------
    "Software Engineering & Application Modernization": [
        "Junior Frontend Developer",
        "Frontend Developer",
        "Senior Frontend Developer",
        "Junior Backend Engineer",
        "Backend Engineer",
        "Senior Backend Engineer",
        "Junior Full-Stack Engineer",
        "Full-Stack Engineer",
        "Senior Full-Stack Engineer",
        "Lead Software Engineer",
        "Software Architect",
    ],
    "Cloud Infrastructure & Platforms": [
        "Junior DevOps Engineer",
        "DevOps Engineer",
        "Senior DevOps Engineer",
        "Junior Cloud Engineer",
        "Cloud Solutions Architect",
        "Site Reliability Engineer (SRE)",
        "Systems Administrator",
    ],
    "Cybersecurity & Digital Identity": [
        "Junior Security Analyst",
        "SOC Analyst",
        "Cybersecurity Engineer",
        "Penetration Tester",
        "IAM Specialist",
        "GRC Consultant",
    ],
    "Data Analytics, AI & Business Intelligence": [
        "Junior Data Analyst",
        "Data Analyst",
        "Junior Data Engineer",
        "Data Engineer",
        "Senior Data Engineer",
        "Machine Learning Engineer",
        "AI/ML Research Scientist",
        "BI Developer",
    ],
    "Quality Assurance & Test Automation": [
        "Junior QA Tester",
        "QA Automation Engineer",
        "Senior QA Automation Engineer",
        "Performance Test Specialist",
        "Test Lead",
    ],
    "IT Service Management & Workplace Operations": [
        "IT Service Desk Specialist (L1/L2)",
        "Senior Service Desk Engineer (L3)",
        "Incident & Problem Manager",
        "Service Delivery Manager",
        "Workplace Support Technician",
        "IT Operations Lead",
    ],
    "Digital Consulting & Transformation Advisory": [
        "Associate Consultant",
        "Technology Consultant",
        "Senior Digital Consultant",
        "Consulting Manager",
        "Solutions Architect",
    ],
    "Product Management & UX/UI Design": [
        "Junior UI/UX Designer",
        "UI/UX Designer",
        "Senior Product Designer",
        "Product Owner",
        "Technical Product Manager",
    ],
    "Enterprise Architecture & Solutions Design": [
        "Associate Solutions Architect",
        "Enterprise Architect",
        "Chief Solutions Architect",
        "Domain Architect (Cloud/Data/Security)",
        "Integration Architect",
        "Technology Strategy Consultant",
    ],
    # ---------------------------------------------------------
    # Corporate & Enabling Functions
    # ---------------------------------------------------------
    "Human Resources & Talent Acquisition": [
        "Talent Acquisition Specialist",
        "HR Operations Specialist",
        "HR Business Partner",
        "Learning & Development Specialist",
        "Compensation & Benefits Analyst",
    ],
    "Finance, Legal & Corporate Governance": [
        "Financial Analyst",
        "Senior Corporate Accountant",
        "Legal Counsel / Contract Specialist",
        "Compliance & Regulatory Officer",
        "Tax & Treasury Specialist",
        "Financial Controller",
    ],
    "Sales, Presales & Account Management": [
        "Business Development Representative (BDR)",
        "Account Executive",
        "Senior Key Account Manager",
        "Presales Solution Consultant",
        "Bid & Proposal Manager",
        "Sales Director",
    ],
    "Project Management Office (PMO)": [
        "PMO Analyst",
        "Scrum Master",
        "Junior Project Manager",
        "Project Manager",
        "Senior Project Manager",
        "Program Director",
    ],
    "Internal IT & Information Security": [
        "Internal Systems Administrator",
        "Network & Systems Engineer",
        "Internal IT Support Specialist",
        "Information Security Analyst",
        "Endpoint Management Specialist",
        "Internal IT Infrastructure Lead",
    ],
    "Marketing & Corporate Communications": [
        "Content Marketing Specialist",
        "Digital Marketing Manager",
        "Corporate Communications Specialist",
        "Brand & Public Relations Manager",
        "Event & Campaign Coordinator",
        "Internal Communications Officer",
    ],
    "Procurement & Supply Chain Management": [
        "Procurement Specialist",
        "IT Vendor Manager",
        "Sourcing & Contract Specialist",
        "Supply Chain Analyst",
        "Category Manager (Hardware & Software)",
        "Purchasing Officer",
    ],
}

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

if "user_id" not in st.session_state:
    st.session_state.user_id = "EMP-0042"  # Placeholder for HR manager's employee ID

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

st.title("📝 Employee Onboarding Intake")
st.caption("Submit new hire details to initiate the automated provisioning pipeline.")

col1, col2 = st.columns(2)

with col1:
    first_name = st.text_input(label="First Name")
    department = st.selectbox(
        label="Department",
        options=DEPARTMENTS,
        index=0,
    )
    location = st.selectbox(
        label="Location (Country, City)",
        options=["Romania, Timisoara", "France, Paris", "China, Beijing"],
    )
    work_location = st.selectbox(
        label="Work Location", 
        options=["remote", "on-site", "hybrid"]
    )

with col2:
    last_name = st.text_input(label="Last Name")
    # Dynamically gets the mapped roles for the selected department
    available_roles = DEPARTMENT_ROLE_MAPPING.get(department, [])
    role = st.selectbox(
        label="Role",
        options=available_roles,
    )
    start_date = st.date_input(label="Start Date")
    employment_type = st.selectbox(
        label="Employment Type", 
        options=["full-time", "part-time", "contract"]
    )

notes = st.text_area(label="Additional Onboarding Notes")
st.caption("⚠️ All fields are required except for 'Additional Onboarding Notes'.")

if st.button(label="Initiate Onboarding", type="primary"):
    # Validation logic
    if not all((first_name, last_name, department, location, work_location, role, start_date, employment_type)):
        st.error("Please fill in all required fields.")
    else:
        payload = {
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "department": department,
            "role": role,
            "location": location,
            "work_location": work_location,
            "start_date": str(start_date),
            "employment_type": employment_type,
            "hr_manager_id": st.session_state.user_id,
            "notes": notes.strip(),
        }
        try:
            res = requests.post(f"{API_URL}/onboarding/requests", json=payload, timeout=10)
            if res.status_code == 200:
                data = res.json()
                st.success(f"Onboarding pipeline started for **{first_name} {last_name}** .")
            else:
                st.error(f"Failed to submit: {res.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not reach backend service.")