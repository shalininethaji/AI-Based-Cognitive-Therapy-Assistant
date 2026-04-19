import streamlit as st
import pandas as pd
from db import get_connection, list_all_therapists, list_all_patients

# --- SECURITY CHECK ---
if st.session_state.get("role") != "admin":
    st.error("Unauthorized access. Admin privileges required.")
    st.stop()

st.title("🎡 Super Admin Control Center")
st.write("Welcome to the cross-platform management dashboard.")

# --- ANALYTICS OVERVIEW ---
st.subheader("📊 System Overview")
conn = get_connection()
if conn:
    col1, col2, col3 = st.columns(3)
    
    # Total Users
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    col1.metric("Total Users", total_users)
    
    # Total Sessions
    cur.execute("SELECT COUNT(*) FROM therapist_inputs")
    total_sessions = cur.fetchone()[0]
    col2.metric("Total Clinical Intake Sessions", total_sessions)
    
    # Total Chat Messages
    cur.execute("SELECT COUNT(*) FROM chat_history")
    total_messages = cur.fetchone()[0]
    col3.metric("Total AI Chat Messages", total_messages)
    
    cur.close()
    conn.close()

st.divider()

# --- THERAPIST MANAGEMENT ---
st.subheader("🩺 Therapist Management")
therapists = list_all_therapists()
if therapists:
    df_therapists = pd.DataFrame(therapists, columns=["ID", "Username", "Joined Date"])
    
    # Use a loop to create a list with delete buttons
    for index, row in df_therapists.iterrows():
        col_id, col_name, col_date, col_action = st.columns([1, 3, 3, 2])
        col_id.write(row["ID"])
        col_name.write(row["Username"])
        col_date.write(row["Joined Date"].strftime("%Y-%m-%d %H:%M"))
        
        # Don't allow admin to delete themselves if they are in the list
        if row["Username"] != st.session_state.get("username"): 
            if col_action.button("Delete", key=f"del_{row['ID']}"):
                from db import delete_user
                if delete_user(row["ID"]):
                    st.success(f"Deleted therapist: {row['Username']}")
                    st.rerun()
                else:
                    st.error("Failed to delete user.")
        else:
            col_action.write(" (Active Admin) ")
else:
    st.info("No therapists registered yet.")

st.divider()

# --- PATIENT OVERVIEW ---
st.subheader("🧘 Platform-wide Patient Activity")
patients = list_all_patients()
if patients:
    df_patients = pd.DataFrame(patients, columns=["Patient ID", "Name", "Assigned Therapist ID", "Session Date"])
    
    # Join with therapist usernames for better display
    # This is a bit advanced for a simple list, but let's keep it simple for now
    st.dataframe(df_patients, use_container_width=True)
else:
    st.info("No patient sessions recorded yet.")

# --- DATABASE MANAGEMENT (OPTIONAL) ---
# st.subheader("⚙️ System Maintenance")
# if st.button("Download System Backup (CSV)"):
#     st.write("Generating backup...")
#     # Logic to export all tables to CSV could go here
