import streamlit as st
import os
from backend.database import track_status_by_app_id, track_status_by_hrms_id  

def track_complaint_status():
    st.markdown("### 🔍 Track Complaint Status")

    search_option = st.selectbox("Search by:", ("Application ID", "HRMS ID"))

    search_input = st.text_input(f"Enter your {search_option}")

    if st.button("Track Status"):
        if search_input.strip() == "":
            st.warning(f"⚠️ Please enter a valid {search_option}.")
        else:
            if search_option == "Application ID":
                complaint = track_status_by_app_id(search_input.strip().upper())

                if complaint:
                    show_complaint(complaint)
                else:
                    st.error("❌ No complaint found for this Application ID.")

            else:  # HRMS ID
                complaints = track_status_by_hrms_id(search_input.strip().upper())
                if complaints:
                    for i, complaint in enumerate(complaints, 1):
                        st.markdown(f"---\n### 📝 Complaint #{i}")
                        show_complaint(complaint)
                else:
                    st.error("❌ No complaints found for this HRMS ID.")

# Helper function to display complaint details
def show_complaint(complaint):
    name, dept, category, desc, date, status, file_path = complaint
    st.write(f"👤 **Name**: {name}")
    st.write(f"🏢 **Department**: {dept}")
    st.write(f"🗂️ **Category**: {category}")
    st.write(f"📝 **Description**: {desc}")
    st.write(f"📅 **Date**: {date}")
    st.write(f"📌 **Status**: `{status}`")

    # Show file if available, else just mention it's not attached
    if file_path:
        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[-1].lower()

            if ext in [".png", ".jpg", ".jpeg"]:
                st.image(file_path, caption="📎 Attached Image", use_container_width=True)

            elif ext == ".pdf":
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="📄 Download PDF",
                        data=f.read(),
                        file_name=os.path.basename(file_path),
                        mime="application/pdf"
                    )
            else:
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"📎 Download File ({os.path.basename(file_path)})",
                        data=f.read(),
                        file_name=os.path.basename(file_path),
                        mime="application/octet-stream"
                    )
        else:
            st.info("ℹ️ File path was provided but the file was not found.")
    else:
        st.info("📎 No file was attached to this complaint.")
