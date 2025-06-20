import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database import fetch_complaints, update_status, delete_complaint
import pandas as pd 

def convert_to_csv(complaints):
    # Convert complaint data to DataFrame
    df = pd.DataFrame(complaints, columns=[
        "ID", "Name", "Employee ID", "Email", "Category",
        "Description", "Date", "Status"
    ])
    return df.to_csv(index=False).encode('utf-8')


def admin_login():
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", key="admin_login_btn"):
        if username == "addy" and password == "12345":
            st.success("Login successful!")

            # Use session_state to persist login
            st.session_state["admin_logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid username or password")
            return

    if st.session_state.get("admin_logged_in", False):
        complaints = fetch_complaints()

        for complaint in complaints:
            cid, name, emp_id, email, category, description, date, status = complaint

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

                col_done, col_delete = st.columns(2)

                with col_done:
                    if status == "Pending":
                        if st.button("✅ Mark as Done", key=f"done_btn_{cid}"):
                            update_status(cid, "Done")
                            st.success(f"Complaint #{cid} marked as Done.")
                            st.rerun()
                    else:
                        st.info("✅ Already marked as Done.")

                with col_delete:
                    if st.button("🗑️ Delete", key=f"delete_btn_{cid}"):
                        if status=="Done":
                            delete_complaint(cid)
                            st.warning(f"Complaint #{cid} deleted.")
                            st.rerun()
                        else:
                            st.error("Cannot delete a pending complaint.")
            
        if complaints:
            csv_data = convert_to_csv(complaints)
            st.download_button(
                    label="📥 Download All Complaints as CSV",
                    data=csv_data,
                    file_name='complaints_report.csv',
                    key="download_csv_1",
                    mime='text/csv'
                )

