import streamlit as st
from datetime import datetime
from backend.database import insert_complaint

valid_user_ids = ["EMP001", "EMP002", "EMP003"]  # List of valid employee IDs

def user_login():
    st.markdown("### 📝 Submit a Complaint")

    # Initialize form-submitted flag
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # Show form only if not submitted
    if not st.session_state.form_submitted:
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
                if not all([name.strip(), emp_id.strip(), email.strip(), description.strip()]):
                    st.error("❌ Please fill in all the fields.")
                elif emp_id.upper().strip() not in valid_user_ids:
                    st.error("❌ Invalid Employee ID. Please enter a valid ID.")
                else:
                    insert_complaint(name, emp_id, email, department, category, description, date)
                    st.success(f"✅ Complaint submitted successfully on {date}! Status: Pending")
                    st.info("Our IT support team will review and respond shortly.")
                    st.session_state.form_submitted = True
                    st.rerun()


    else:
        st.success("✅ Your complaint has already been submitted.")
        if st.button("Submit Another Complaint"):
            st.session_state.form_submitted = False
            st.rerun()

    # --- Footer ---
    st.markdown("---")
    st.markdown("© 2025 North Western Railway | Managed by IT Cell")
