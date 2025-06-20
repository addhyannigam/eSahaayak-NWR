import streamlit as st
from backend.database import track_status_by_emp_id

def track_complaint_status():
    st.markdown("### 🔍 Track Complaint Status")

    emp_id = st.text_input("Enter your Employee ID to check complaint status")

    if st.button("Track Status"):
        if emp_id.strip() == "":
            st.warning("Please enter a valid Employee ID")
        else:
            complaints = track_status_by_emp_id(emp_id)
            if complaints:
                for comp in complaints:
                    category, description, status = comp
                    st.info(f"🗂️ **Category**: {category}\n\n📝 **Description**: {description}\n\n📌 **Status**: `{status}`")
            else:
                st.warning("No complaints found for this Employee ID.")
