import streamlit as st
from PIL import Image
from datetime import datetime
import base64
import admin
import users

st.set_page_config(page_title="eSahaayak NWR", page_icon="design/logo.png", layout="centered")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "selected_role" not in st.session_state:
    st.session_state.selected_role = None
if "previous_role" not in st.session_state:
    st.session_state.previous_role = None

# --- Logo ---
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

# --- Login ---
valid_user_ids = ["EMP001", "EMP002", "EMP003"]

if not st.session_state.logged_in:
    st.markdown("### 🔐 Enter Your Employee ID to Proceed")
    user_id = st.text_input("Employee ID")
    if st.button("Login"):
        if user_id.upper() in [uid.upper() for uid in valid_user_ids]:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id.upper()
            st.success("✅ Login successful.")
            st.rerun()
        else:
            st.error("❌ Invalid Employee ID")

# --- After login ---
if st.session_state.logged_in:
    st.sidebar.markdown("## Select Role")
    selected = st.sidebar.selectbox("Choose Role", ["Users", "Admin"])
    
    # 🔄 Reset admin login if role has changed from Admin to something else
    if st.session_state.previous_role == "Admin" and selected != "Admin":
        st.session_state.admin_logged_in = False

    # ✅ Update current selected role
    st.session_state.selected_role = selected
    st.session_state.previous_role = selected

    # --- USER ROLE ---
    if selected == "Users":
        users.user_login()

    # --- ADMIN ROLE ---
    elif selected == "Admin":
        if not st.session_state.admin_logged_in:
            st.markdown("### 🔐 Admin Login Required")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login as Admin"):
                if username == "addy" and password == "12345":
                    st.success("✅ Admin access granted.")
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect admin credentials.")
        else:
            admin.admin_login()

# --- Logout Button ---
if st.session_state.logged_in:
    if st.sidebar.button("🔒 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
