import streamlit as st
from backend.database import track_status_by_app_id

def track_complaint_status():
    st.markdown("### 🔍 Track Complaint Status by Application ID")

    application_id = st.text_input("Enter your Application ID")

    if st.button("Track Status"):
        if application_id.strip() == "":
            st.warning("⚠️ Please enter a valid Application ID.")
        else:
            complaint = track_status_by_app_id(application_id.strip().upper())
            if complaint:
                name, dept, category, desc, date, status = complaint
                st.success("✅ Complaint Found:")
                st.write(f"👤 **Name**: {name}")
                st.write(f"🏢 **Department**: {dept}")
                st.write(f"🗂️ **Category**: {category}")
                st.write(f"📝 **Description**: {desc}")
                st.write(f"📅 **Date**: {date}")
                st.write(f"📌 **Status**: `{status}`")
            else:
                st.error("❌ No complaint found for this Application ID.")
