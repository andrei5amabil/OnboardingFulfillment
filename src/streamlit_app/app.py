import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(page_title="Employee Onboarding System", layout="wide")

# Define distinct functional views
hr_page = st.Page("pages/hr.py", title="New Hire Intake", icon="📝")
it_page = st.Page("pages/it.py", title="IT Approvals & Tasks", icon="🛠️")

# Group pages in navigation
pg = st.navigation({
    "HR Portal": [hr_page],
    "IT Operations": [it_page]
})

pg.run()