import streamlit as st
from backend.database import track_status_by_hrms_id

def track_complaint_status():
    st.markdown("### 🔍 Track Complaint Status")

    hrms_id = st.text_input("Enter your HRMS ID to check complaint status")

    if st.button("Track Status"):
        if hrms_id.strip() == "":
            st.warning("Please enter a valid HRMS ID")
        else:
            complaints = track_status_by_hrms_id(hrms_id)
            if complaints:
                for comp in complaints:
                    category, description, status = comp
                    st.info(f"🗂️ **Category**: {category}\n\n📝 **Description**: {description}\n\n📌 **Status**: `{status}`")
            else:
                st.warning("No complaints found for this HRMS ID.")
