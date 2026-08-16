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
                st.markdown(f"### {task.get('full_name')} — `{task.get('role')}`")
                st.write(f"**Department:** {task.get('department')} | **Hardware:** {task.get('hardware_tier')}")
                st.write(f"**Status:** `{task.get('status')}`")
            
            with col_action:
                st.write("")
                if st.button("Approve & Provision", key=f"btn_{task.get('id')}", type="primary"):
                    approval_res = requests.post(
                        f"{API_URL}/onboarding/{task.get('id')}/approve",
                        json={"status": "approved"},
                        timeout=5
                    )
                    if approval_res.status_code == 200:
                        st.toast(f"Approved provisioning for {task.get('full_name')}!")
                        st.rerun()
                    else:
                        st.error("Failed to approve task.")