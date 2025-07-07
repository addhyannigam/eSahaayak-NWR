import streamlit as st
import pandas as pd 
from datetime import datetime
from backend.database import insert_complaint

valid_user_ids = pd.read_csv("hrms_ids.csv")["HRMS ID"].astype(str).tolist() # List of valid employee IDs

def user_login():
    st.markdown("### 📝 Submit a Complaint")

    # Initialize form-submitted flag
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # Show form only if not submitted
    if not st.session_state.form_submitted:
        with st.form("complaint_form"):
            name = st.text_input("Your Name")
            hrms_id = st.text_input("HRMS ID")
            department = st.selectbox("Department", ["General", "Administration", "Accounts Department", "Commercial",
                                        "Construction", "Electrical Department", "Engineering", "IT Centre", 
                                        "Mechanical", "Medical", "Operating Department", "Personnel Department", "Rajbhasha", 
                                        "Safety Department", "Security Department", "Signal & Telecom", "Stores Department"
                                        ,"Vigilance Department"])
            
            category = st.selectbox("Complaint Category", ["eOffice", "IR-WCMS", "IRPSM", "ANTIVIRUS", "eOffice", "HMIS", "HRMS",
                                                           "HARDWARE (COMPUTER- PRINTER-UPS)", "IPAS (AIMS)", "IREPS / UDM", "NIC MAIL",
                                                           "NETWORKING", "NETWORKING (another entry, possibly different level)",
                                                           "ORH-PRAVAS", "SPARROW", 'others'])
            
            description = st.text_area("Describe the Issue")
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            submitted = st.form_submit_button("Submit Complaint")

            if submitted:
                if not all([name.strip(), hrms_id.strip(), description.strip()]):
                    st.error("❌ Please fill in all the fields.")
                elif hrms_id.upper().strip() not in valid_user_ids:
                    st.error("❌ Invalid HRMS ID. Please enter a valid ID.")
                else:
                    insert_complaint(name, hrms_id, department, category, description, date)
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
