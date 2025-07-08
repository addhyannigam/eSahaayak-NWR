import streamlit as st
import pandas as pd 
import os
from datetime import datetime
from backend.database import insert_complaint

# Load valid HRMS IDs
valid_user_ids = pd.read_csv("hrms_ids.csv")["HRMS ID"].astype(str).tolist()

def user_login():
    st.markdown("### 📝 Submit a Complaint")

    # Session flags
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    if "submitted_info" not in st.session_state:
        st.session_state.submitted_info = {}

    # Show form if not submitted
    if not st.session_state.form_submitted:
        with st.form("complaint_form"):
            name = st.text_input("Your Name")
            hrms_id = st.text_input("HRMS ID")
            
            department = st.selectbox("Department", [
                "General", "Administration", "Accounts Department", "Commercial",
                "Construction", "Electrical Department", "Engineering", "IT Centre", 
                "Mechanical", "Medical", "Operating Department", "Personnel Department", 
                "Rajbhasha", "Safety Department", "Security Department", "Signal & Telecom", 
                "Stores Department", "Vigilance Department"
            ])
            
            category = st.selectbox("Complaint Category", [
                "eOffice", "IR-WCMS", "IRPSM", "ANTIVIRUS", "HMIS", "HRMS",
                "HARDWARE (COMPUTER- PRINTER-UPS)", "IPAS (AIMS)", "IREPS / UDM", 
                "NIC MAIL", "NETWORKING", "NETWORKING (another entry, possibly different level)",
                "ORH-PRAVAS", "SPARROW", 'others'
            ])
            
            description = st.text_area("Describe the Issue")

            # ✅ File Upload
            uploaded_file = st.file_uploader("📎 Attach Screenshot / Document (optional)", type=["png", "jpg", "jpeg", "pdf"])

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            submitted = st.form_submit_button("Submit Complaint")

            if submitted:
                if not all([name.strip(), hrms_id.strip(), description.strip()]):
                    st.error("❌ Please fill in all the fields.")
                elif hrms_id.upper().strip() not in valid_user_ids:
                    st.error("❌ Invalid HRMS ID. Please enter a valid ID.")
                else:
                    # ✅ Save file if uploaded
                    file_path = None
                    if uploaded_file:
                        upload_dir = "uploaded_files"
                        os.makedirs(upload_dir, exist_ok=True)
                        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
                        file_path = os.path.join(upload_dir, filename)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                    # ✅ Insert complaint with optional file_path 
                    application_id = insert_complaint(name, hrms_id, department, category, description, date, file_path)
                    st.session_state.form_submitted = True
                    st.session_state.submitted_info = {
                        "application_id": application_id,
                        "date": date
                    }
                    st.rerun()

    # Show confirmation after submission
    else:
        info = st.session_state.get("submitted_info", {})
        if info:
            st.success(f"✅ Complaint submitted successfully on {info['date']}!")
            st.info(f"📌 **Your Application ID is:** `{info['application_id']}`")
            st.write("🔍 Use this ID to track your complaint status on the tracking page.")
        else:
            st.success("✅ Your complaint has already been submitted.")

        if st.button("Submit Another Complaint"):
            st.session_state.form_submitted = False
            st.session_state.submitted_info = {}
            st.rerun()

    # --- Footer ---
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.9em;'>
            © 2025 North Western Railway | Managed by <b>IT Cell</b>
        </div>
        """,
        unsafe_allow_html=True
    )
