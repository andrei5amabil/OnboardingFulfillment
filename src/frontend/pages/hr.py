import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

if "user_id" not in st.session_state:
    st.session_state.user_id = "HR-001"

st.title("📝 Employee Onboarding Intake")
st.caption("Submit new hire details to initiate the automated provisioning pipeline.")

with st.form("new_employee_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input(label="First Name")
        department = st.selectbox(label="Department", options=["engineering", "product", "sales", "design", "hr", "it", "management"])
        location = st.selectbox(label="Location(Country, City)", options=["Romania, Timisoara", "France, Paris", "China, Beijing"])
        work_location = st.selectbox(label="Work Location", options=["remote", "on-site", "hybrid"])
    
    with col2:
        last_name = st.text_input(label="Last Name")
        role = st.text_input(label="Role")
        start_date = st.date_input(label="Start Date")
        employment_type = st.selectbox(label="Employment Type", options=["full-time", "part-time", "contract"])

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
            "hr_manager_id": st.session_state.user_id,
            "notes": notes
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