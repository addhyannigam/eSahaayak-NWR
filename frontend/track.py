import streamlit as st
import os
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
                name, dept, category, desc, date, status, file_path = complaint
                st.success("✅ Complaint Found:")
                st.write(f"👤 **Name**: {name}")
                st.write(f"🏢 **Department**: {dept}")
                st.write(f"🗂️ **Category**: {category}")
                st.write(f"📝 **Description**: {desc}")
                st.write(f"📅 **Date**: {date}")
                st.write(f"📌 **Status**: `{status}`")

                # File preview or download
                if file_path and os.path.exists(file_path):
                    file_ext = os.path.splitext(file_path)[-1].lower()

                    if file_ext in [".png", ".jpg", ".jpeg"]:
                        st.image(file_path, caption="📎 Attached Image", use_container_width=True)

                    elif file_ext == ".pdf":
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📄 Download Attached PDF",
                                data=f.read(),
                                file_name=os.path.basename(file_path),
                                mime="application/pdf"
                            )
                    else:
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label=f"📎 Download Attached File ({os.path.basename(file_path)})",
                                data=f.read(),
                                file_name=os.path.basename(file_path),
                                mime="application/octet-stream"
                            )

            else:
                st.error("❌ No complaint found for this Application ID.")
