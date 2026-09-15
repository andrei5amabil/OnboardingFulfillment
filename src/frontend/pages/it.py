import os
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

if "user_id" not in st.session_state:
    st.session_state.user_id = "EMP-IT-01"

st.title("🛠️ IT Provisioning & Approvals")
st.caption("Review agent-generated access plans, request revisions, or commit deterministic provisioning.")
col_title, col_ref = st.columns([4, 1])
with col_ref:
    if st.button("🔄 Refresh View", use_container_width=True):
        st.rerun()
try:
    res = requests.get(f"{API_URL}/onboarding/requests", timeout=60)
    pending_tasks = res.json() if res.status_code == 200 else []
except requests.exceptions.ConnectionError:
    st.error("Could not load pending tasks from backend.")
    pending_tasks = []

if not pending_tasks:
    st.info("No actions awaiting IT approval.")
else:
    pending_tasks = [task for task in pending_tasks if task.get("status") != "completed"]
    for task in pending_tasks:
        req_id = task.get("request_id")
        runs = task.get("workflow_runs") or []
        current_status = task.get("status")
        has_plan = len(runs) > 0

        with st.container(border=True):
            st.markdown(f"### {task.get('first_name')} {task.get('last_name')}")
            st.write(f"**Request ID:** `{req_id}` | **Status:** `{current_status}`")
            st.write(f"**Department:** {task.get('department')} | **Role:** {task.get('role')}")
            st.write(f"**Work Location:** `{task.get('work_location')}`")

            st.divider()

            if current_status == "processing_rules":
                st.info("⏳ Agent is generating the plan and checking compliance policies (takes ~10-15s)...")
                if st.button("🔄 Check Status", key=f"btn_check_{req_id}"):
                    st.rerun()
            elif current_status == "failed":
                st.error("❌ Plan generation failed in the background.")
                if st.button("🔄 Retry Plan Generation", key=f"btn_retry_{req_id}"):
                    requests.post(f"{API_URL}/onboarding/requests/{req_id}/generate-plan", timeout=10)
                    st.rerun()
            elif current_status == "requires_manual_intervention":
                st.error("🚨 Maximum revision attempts reached (3/3). This request requires manual IT handling.")
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
                    st.dataframe(pd.DataFrame(flattened), width='stretch', hide_index=True)

                hardware = plan.get("suggested_hardware", {})
                st.markdown("**💻 Suggested Hardware Provisioning**")
                if hardware:
                    st.json(hardware)
                else:
                    st.warning("No hardware provisioning rules generated.")

                citations = plan.get("policy_citations", [])
                if citations:
                    st.markdown("**🛡️ Policy Citations & Flags**")
                    st.json(citations)

                # --- HITL Review Actions ---
                if current_status == "pending_approval":
                    st.divider()
                    st.markdown("#### ⚖️ IT Review Decision")

                    feedback_note = st.text_area(
                        "Revision Notes / Feedback (Required if regenerating)",
                        key=f"note_{req_id}",
                        placeholder="e.g., Provide 32GB RAM model instead",
                    )

                    col_regen, col_approve = st.columns(2)

                    with col_regen:
                        if st.button("🔄 Regenerate Plan", key=f"btn_regen_{req_id}", width='stretch'):
                            with st.spinner("Requesting plan revision from agent..."):
                                review_body = {
                                    "action": "regenerate",
                                    "note": feedback_note.strip(),
                                    "reviewed_by": st.session_state.user_id,
                                }
                                review_res = requests.post(
                                    f"{API_URL}/onboarding/requests/{req_id}/review",
                                    json=review_body,
                                    timeout=60,
                                )
                                if review_res.status_code == 200:
                                    st.rerun()
                                else:
                                    st.error(f"Failed to request revision: {review_res.json().get('detail')}")

                    with col_approve:
                        if st.button("🚀 Approve & Provision", key=f"btn_app_{req_id}", type="primary", width='stretch'):
                            with st.spinner("Executing deterministic provisioning to database..."):
                                review_body = {
                                    "action": "approve",
                                    "note": feedback_note.strip(),
                                    "reviewed_by": st.session_state.user_id,
                                }
                                review_res = requests.post(
                                    f"{API_URL}/onboarding/requests/{req_id}/review",
                                    json=review_body,
                                    timeout=30,
                                )
                                if review_res.status_code == 200:
                                    st.success("Employee record and licenses provisioned successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Provisioning failed: {review_res.json().get('detail')}")
            elif current_status == "pending_onboarding" and not has_plan:
                st.warning("⚠️ Request intake received, but plan generation has not executed.")
                if st.button("⚙️ Launch Agent Planner", key=f"btn_start_{req_id}", type="primary"):
                    with st.spinner("Starting agent workflow..."):
                        res = requests.post(f"{API_URL}/onboarding/requests/{req_id}/generate-plan", timeout=10)
                        if res.status_code == 200:
                            st.rerun()
                        else:
                            st.error("Failed to trigger agent.")
            elif current_status == "completed":
                st.success("✅ Provisioning finalized. Active employee and software records written to database.")