import streamlit as st
from db import authenticate_user, register_user

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI CBT Therapy", page_icon="🧠", layout="wide")

# --- SESSION STATE ---
if "role" not in st.session_state:
    st.session_state.role = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "patient_id" not in st.session_state:
    st.session_state.patient_id = None
if "show_reg" not in st.session_state:
    st.session_state.show_reg = False

# --- AUTH LOGIC ---
def login():
    st.title("🧠 AI CBT Therapy Portal")
    
    tab1, tab2 = st.tabs(["Therapist Portal", "Patient Access"])
    
    with tab1:
        if not st.session_state.show_reg:
            st.subheader("Therapist Login")
            username = st.text_input("Username", key="t_user")
            password = st.text_input("Password", type="password", key="t_pass")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("Login"):
                    user_data = authenticate_user(username, password)
                    if user_data:
                        st.session_state.role = user_data["role"]
                        st.session_state.user_id = user_data["id"]
                        st.session_state.username = username
                        st.session_state.patient_id = user_data["patient_id"]
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            
            st.divider()
            st.write("Don't have an account?")
            if st.button("Register as Therapist"):
                st.session_state.show_reg = True
                st.rerun()
        
        else:
            st.subheader("Therapist Registration")
            new_user = st.text_input("New Username", key="reg_user")
            new_pass = st.text_input("New Password", type="password", key="reg_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register"):
                if new_user and new_pass:
                    if new_pass == confirm_pass:
                        if register_user(new_user, new_pass, "therapist"):
                            st.success("Registration successful! Please login.")
                            st.session_state.show_reg = False
                            st.rerun()
                        else:
                            st.error("Registration failed. Username might already exist.")
                    else:
                        st.error("Passwords do not match.")
                else:
                    st.warning("Please fill in all fields.")
            
            if st.button("Back to Login"):
                st.session_state.show_reg = False
                st.rerun()

    with tab2:
        st.subheader("Enter your Patient ID")
        patient_id = st.text_input("Patient ID", key="p_id")
        if st.button("Start Session"):
            if patient_id:
                from db import get_connection
                conn = get_connection()
                if conn:
                    cur = conn.cursor()
                    cur.execute("SELECT patient_id FROM therapist_inputs WHERE patient_id=%s", (patient_id,))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()
                    
                    if result:
                        st.session_state.role = "patient"
                        st.session_state.patient_id = patient_id
                        st.rerun()
                    else:
                        st.error("❌ Patient ID not found.")
                else:
                    st.error("Database connection failed.")
            else:
                st.warning("Please enter your Patient ID")

def logout():
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.patient_id = None
    st.rerun()

# --- NAVIGATION ---
login_page = st.Page(login, title="Login", icon="🔐")
logout_page = st.Page(logout, title="Logout", icon="🚪")

# Define pages from files
admin_page = st.Page("pages/0_admin.py", title="Admin Control Center", icon="🎡")
input_page = st.Page("pages/1_input.py", title="Clinical Intake", icon="🩺")
chat_page = st.Page("pages/2_chat.py", title="Personal CBT Chat", icon="🧘")
dashboard_page = st.Page("pages/3_dashboard.py", title="Therapist Dashboard", icon="📊")

# Dynamic Menu Logic
if st.session_state.role == "admin":
    pg = st.navigation([admin_page, logout_page])
elif st.session_state.role == "therapist":
    pg = st.navigation([input_page, dashboard_page, logout_page])
elif st.session_state.role == "patient":
    pg = st.navigation([chat_page, logout_page])
else:
    pg = st.navigation([login_page])

pg.run()