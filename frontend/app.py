import streamlit as st
from PIL import Image
from datetime import datetime
import base64
import admin
import users

st.set_page_config(page_title="eSahaayak NWR", page_icon="design/logo.png", layout="centered")

# --- Session State to track login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

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

# --- Login Flow ---
valid_user_ids = ["EMP001", "EMP002", "EMP003"]

if not st.session_state.logged_in:
    st.markdown("### 🔐 Enter Your Employee ID to Proceed")
    user_id = st.text_input("Employee ID")
    if st.button("Login"):
        if user_id.upper() in [uid.upper() for uid in valid_user_ids]:
            st.session_state.logged_in = True
            st.success("✅ Login successful.")
        else:
            st.error("❌ Invalid Employee ID. Please try again.")

# --- Show Sidebar AFTER login ---
if st.session_state.logged_in:
    st.sidebar.markdown("## Select Role")
    role = st.sidebar.selectbox("Choose Role", ["Users", "Admin"])

    # Show User Page
    if role == "Users":
        st.session_state.role = "Users"
        users.user_login()

    # Show Admin Page
    elif role == "Admin":
        st.session_state.role = "Admin"
        admin.admin_login()
