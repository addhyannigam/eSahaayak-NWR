import streamlit as st
import pandas as pd 
from PIL import Image
import base64
import admin
import users
import track

# --- App Configuration ---
st.set_page_config(page_title="eSahaayak NWR", page_icon="design/logo.png", layout="centered")

# --- Initialize Session State Safely ---
default_session_values = {
    "logged_in": False,
    "user_id": None,
    "admin_logged_in": False,
    "selected_role": None,
    "previous_role": None,
    "admin_username": None,
    "admin_role": None
}

for key, val in default_session_values.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- Logo Display ---
with open("design/logo3.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{encoded_string}" width="500" style="margin-bottom: 20px;" />
    </div>
    """,
    unsafe_allow_html=True
)

# --- User Authentication ---
valid_users_df = pd.read_csv("hrms_ids.csv")  
valid_user_ids = valid_users_df["HRMS ID"].astype(str).tolist()

if not st.session_state.logged_in:
    st.markdown("### 🔐 Enter Your HRMS ID to Proceed")
    user_id = st.text_input("HRMS ID")

    if st.button("Login"):
        normalized_id = user_id.strip().upper()

        if normalized_id in valid_user_ids:
            user_name = valid_users_df.loc[valid_users_df["HRMS ID"] == normalized_id, "Name"].values[0]

            # Store both ID and Name in session state
            st.session_state.logged_in = True
            st.session_state.user_id = normalized_id
            st.session_state.user_name = user_name

            st.success(f"✅ Welcome, {user_name}!")
            st.rerun()
        else:
            st.error("❌ Invalid HRMS ID")


# --- Main App Interface ---
if st.session_state.logged_in:
    st.sidebar.markdown("## 📂 Navigation")
    selected = st.sidebar.selectbox("Choose a page", ["Submit Complaint", "Admin Panel", "Track Status"])

    # --- Detect role switch (Admin → non-Admin) and reset admin session ---
    if st.session_state.previous_role == "Admin Panel" and selected != "Admin Panel":
        st.session_state.admin_logged_in = False
        st.session_state.admin_username = None
        st.session_state.admin_role = None

    # Update role tracking
    st.session_state.selected_role = selected
    st.session_state.previous_role = selected

    # --- User Interface: Complaint Submission ---
    if selected == "Submit Complaint":
        users.user_login()

    # --- Admin Interface: Fully handled in admin.py ---
    elif selected == "Admin Panel":
        admin.admin_login()

    # --- Track Complaint Status (Employee View) ---
    elif selected == "Track Status":
        track.track_complaint_status()

    # --- Logout Button ---
    if st.sidebar.button("🔒 Logout"):
        st.session_state.clear() 
        st.rerun()
