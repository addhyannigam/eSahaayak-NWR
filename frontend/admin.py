import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database import fetch_complaints, update_status


# Admin Login Section
def admin_login():
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "addy" and password == "12345":
            st.success("Login successful!")
            
            complaints = fetch_complaints()

            for complaint in complaints:
                cid, name, emp_id, category, description, date, status = complaint

                with st.expander(f"🔎 Complaint #{cid} | {name} ({emp_id}) - {category} [{status}]"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**👤 Name:** {name}")
                        st.markdown(f"**🆔 Employee ID:** {emp_id}")
                        st.markdown(f"**📅 Date:** {date}")

                    with col2:
                        st.markdown(f"**🏢 Department/Category:** {category}")
                        st.markdown(f"**📌 Status:** `{status}`")

                    st.markdown("---")
                    st.markdown(f"**📝 Description:**\n{description}")

                    if status == "Pending":
                        if st.button("✅ Mark as Done", key=f"done_btn_{cid}"):
                            update_status(cid, "Done")
                            st.success("Complaint marked as Done.")
                            st.experimental_rerun()
                    else:
                        st.info("✅ This complaint is already marked as Done.")


        else:
            st.error("Invalid username or password")
            return False
    return False
