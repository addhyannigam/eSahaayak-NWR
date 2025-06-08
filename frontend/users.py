import streamlit as st
from datetime import datetime
from backend.database import insert_complaint

    # --- Complaint Form ---
def user_login():
    
    st.markdown("### 📝 Submit a Complaint")

    with st.form("complaint_form"):
        name = st.text_input("Your Name")
        emp_id = st.text_input("Employee ID")
        email = st.text_input("Email")
        department = st.selectbox("Department", ["Accounts", "Operations", "IT", "HR", "Engineering", "Other"])
        category = st.selectbox("Complaint Category", [
                "eOffice", "SPARROW", "IREPS", "IRPSM", "Antivirus", "Network", "Other"
            ])
        description = st.text_area("Describe the Issue")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        submitted = st.form_submit_button("Submit Complaint")

        if submitted:
            st.info("Our IT support team will review and respond shortly.")
            insert_complaint(name, emp_id, email, department, category, description, date)
            st.success(f"✅ Complaint submitted successfully on {date} ! Status: Pending")

        # --- Footer ---
    st.markdown("---")
    st.markdown("© 2025 North Western Railway | Managed by IT Cell")