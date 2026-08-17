import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("🛠️ IT Provisioning & Approvals")
st.caption("Review pending access approvals and monitor active automation steps.")

# Fetch pending actions
try:
    res = requests.get(f"{API_URL}/onboarding/requests", timeout=5)
    pending_tasks = res.json() if res.status_code == 200 else []
except requests.exceptions.ConnectionError:
    st.error("Could not load pending tasks from backend.")
    pending_tasks = []

if not pending_tasks:
    st.info("No actions awaiting IT approval.")
else:
    for task in pending_tasks:
        with st.container(border=True):
            col_info, col_action = st.columns([3, 1])
            with col_info:
                st.markdown(f"### {task.get('first_name')} {task.get('last_name')}")
                st.write(f"**Department:** {task.get('department')} | **Role:** {task.get('role')}")
                st.write(f"**Status:** `{task.get('status')}`")
                st.write(f"**Approved by HR:** {task.get('hr_manager_id')}")