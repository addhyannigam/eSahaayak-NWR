import streamlit as st
import sys
import os
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database import fetch_complaints, update_status, delete_complaint

# --- CSV Export ---
def convert_to_csv(complaints):
    df = pd.DataFrame(complaints, columns=[
        "ID", "Name", "HRMS ID", "Department", "Category",
        "Description", "Date", "Status"
    ])
    return df.to_csv(index=False).encode('utf-8')

# --- Normalize Helper ---
def normalize(text):
    return text.strip().lower().replace(" department", "").replace("&", "and")

# --- Admin Login Function ---
def admin_login():
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    admin_df = pd.read_csv("admin_users.csv")

    if st.button("Login", key="admin_login_btn"):
        matched_admin = admin_df[
            (admin_df["username"] == username) & (admin_df["password"] == password)
        ]
        if not matched_admin.empty:
            st.success(f"Welcome, {username}!")
            st.session_state["admin_logged_in"] = True
            st.session_state["admin_username"] = username
            st.session_state["admin_role"] = matched_admin.iloc[0]["role"]
            st.session_state["admin_category"] = matched_admin.iloc[0]["category"]
            st.rerun()
        else:
            st.error("Invalid username or password")
            return

    if st.session_state.get("admin_logged_in", False):
        role = st.session_state["admin_role"]
        username = st.session_state["admin_username"]
        category_filter = st.session_state["admin_category"]

        if role == "superadmin" or normalize(category_filter) == "all":
            st.subheader("🌟 Super Admin Dashboard - View All Complaints")
        else:
            st.subheader(f"🔧 {category_filter.upper()} Admin Dashboard")

        # Fetch complaints
        complaints = fetch_complaints()

        # Filter complaints by department
        if normalize(category_filter) != "all":
            complaints = [
                c for c in complaints if normalize(c[3]) == normalize(category_filter)
            ]

        if not complaints:
            st.warning("🚫 No complaints found for your department.")
            return

        # Show complaints
        for complaint in complaints:
            try:
                cid, name, hrms_id, department, category, description, date, status = complaint
            except ValueError:
                st.error(f"⚠️ Malformed complaint record: {complaint}")
                continue

            with st.expander(f"🔎 Complaint #{cid} | {name} ({hrms_id}) - {category} [{status}]"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**👤 Name:** {name}")
                    st.markdown(f"**🆔 HRMS ID:** {hrms_id}")
                    st.markdown(f"**📅 Date:** {date}")

                with col2:
                    st.markdown(f"**🏢 Department:** {department}")
                    st.markdown(f"**📁 Category:** {category}")
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
                        if status == "Done":
                            delete_complaint(cid)
                            st.warning(f"Complaint #{cid} deleted.")
                            st.rerun()
                        else:
                            st.error("❌ Cannot delete a pending complaint.")

        # Download button
        csv_data = convert_to_csv(complaints)
        st.download_button(
            label="📥 Download Complaints as CSV",
            data=csv_data,
            file_name='complaints_report.csv',
            key="download_csv_1",
            mime='text/csv'
        )
