import os
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("🛠️ IT Provisioning & Approvals")
st.caption("Review pending access approvals and monitor active automation steps.")

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
        req_id = task.get("request_id")
        runs = task.get("workflow_runs") or []
        current_status = task.get("status")
        has_plan = len(runs) > 0

        with st.container(border=True):
            col_info, col_action = st.columns([3, 1])

            with col_info:
                st.markdown(f"### {task.get('first_name')} {task.get('last_name')}")
                st.write(f"**Request ID:** `{req_id}` | **Status:** `{current_status}`")
                st.write(f"**Department:** {task.get('department')} | **Role:** {task.get('role')}")
                st.write(f"**Work Location:** `{task.get('work_location')}`")

            with col_action:
                btn_label = "🔄 Regenerate Plan" if has_plan else "⚙️ Generate Plan"
                if st.button(btn_label, key=f"btn_gen_{req_id}", use_container_width=True):
                    try:
                        gen_res = requests.post(f"{API_URL}/onboarding/requests/{req_id}/generate-plan", timeout=10)
                        if gen_res.status_code == 200:
                            st.rerun()
                        else:
                            st.error("Failed to generate plan.")
                    except requests.exceptions.ConnectionError:
                        st.error("Backend unreachable.")

            st.divider()

            # Permanent plan view
            if current_status == "processing_rules":
                st.spinner("Processing deterministic assignment rules...")
            elif has_plan:
                plan = runs[0]
                rules = plan.get("suggested_licenses", [])

                st.markdown("**📋 Deterministic Entitlement Plan (SQL Rules)**")
                if not rules:
                    st.warning("No explicit assignment rules found for this role and department.")
                else:
                    flattened = [
                        {
                            "Product": (r.get("software_products") or {}).get("name", "Unknown"),
                            "Vendor": (r.get("software_products") or {}).get("vendor", "N/A"),
                            "License Type": (r.get("software_products") or {}).get("license_type", "N/A"),
                            "Access Level": r.get("access_level"),
                            "Mandatory": "✅" if r.get("is_mandatory") else "❌",
                            "Needs Approval": "Yes" if r.get("requires_approval") else "No",
                        }
                        for r in rules
                    ]
                    st.dataframe(pd.DataFrame(flattened), use_container_width=True, hide_index=True)

                hardware = plan.get("suggested_hardware", {})
                st.markdown("**💻 Suggested Hardware Provisioning**")
                if not hardware:
                    st.warning("No hardware provisioning rules found for this role and department.")
            else:
                st.info("No plan generated yet. Click 'Generate Plan' to trigger.")