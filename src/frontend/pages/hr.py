import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("📝 Employee Onboarding Intake")
st.caption("Submit new hire details to initiate the automated provisioning pipeline.")

with st.form("new_employee_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input(label="First Name")
        department = st.selectbox(label="Department", options=["Engineering", "Product", "Sales", "Design", "HR", "IT", "Management"])
        location = st.text_input(label="Location(Country, City)")
        work_location = st.selectbox(label="Work Location", options=["Remote", "On-site", "Hybrid"])
    
    with col2:
        last_name = st.text_input(label="Last Name")
        role = st.text_input(label="Role")
        start_date = st.date_input(label="Start Date")
        employment_type = st.selectbox(label="Employment Type", options=["Full-time", "Part-time", "Contract"])

    notes = st.text_area(label="Additional Onboarding Notes")
    warning = st.text("⚠️ All fields are required except for 'Additional Onboarding Notes'.")
    submitted = st.form_submit_button(label="Initiate Onboarding", type="primary")

if submitted:
    if not all((first_name, last_name, department, location, work_location, role, start_date, employment_type)):
        st.error("Please fill in all required fields.")
    else:
        payload = {
            "first_name": f"{first_name}",
            "last_name": f"{last_name}",
            "department": department,
            "role": role,
            "start_date": str(start_date),
            "employment_type": employment_type,
            "location": location,
            "work_location": work_location,
            "notes": notes
        }
        
        try:
            res = requests.post(f"{API_URL}/onboarding/requests", json=payload, timeout=10)
            if res.status_code == 200:
                data = res.json()
                st.success(f"Onboarding pipeline started for **{first_name} {last_name}** (Process ID: `{data.get('id', 'N/A')}`).")
            else:
                st.error(f"Failed to submit: {res.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not reach backend service.")