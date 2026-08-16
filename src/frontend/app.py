import streamlit as st

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