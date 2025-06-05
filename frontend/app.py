import streamlit as st
from PIL import Image
from datetime import datetime

# --- App Title and Logo ---
st.set_page_config(page_title="eSahaayak NWR",page_icon="design/logo.png", layout="centered")

image = Image.open("design/logo2.jpg")
resized_image = image.resize((400,150))  # Width: 350px, Height: 200px
st.image(resized_image) 
st.title("🛠 eSahaayak NWR")
st.markdown("जहां तकनीकी समस्याओं का समाधान है एक क्लिक दूर")

# --- Side Bar OPTION ---#
st.sidebar.selectbox("Choose Role", ["Users", "Admin"])


# --- Complaint Form ---
st.markdown("### 📝 Submit a Complaint")

with st.form("complaint_form"):
    name = st.text_input("Your Name")
    emp_id = st.text_input("Employee ID")
    email = st.text_input("Email")
    department = st.selectbox("Department", ["Accounts", "Operations", "IT", "HR", "Engineering", "Other"])
    category = st.selectbox("Complaint Category", [
        "eOffice", "SPARROW", "IREPS", "IRPSM", "Antivirus", "Network", "Other"
    ])
    description = st.text_area("Describe the Issue")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    submitted = st.form_submit_button("Submit Complaint")

    if submitted:
        st.success(f"Complaint submitted successfully on {date}.")
        st.info("Our IT support team will review and respond shortly.")
        # You can later save this to a database or CSV

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 North Western Railway | Managed by IT Cell")