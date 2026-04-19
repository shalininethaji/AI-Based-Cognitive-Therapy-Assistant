import streamlit as st
from db import get_connection
import datetime

if st.session_state.get("role") != "therapist":
    st.error("Unauthorized access")
    st.stop()

# st.set_page_config(page_title="Therapist Portal", page_icon="🩺")
st.title("🩺 Clinical Intake & Examination")

# CSS to make the form look cleaner
st.markdown("""
    <style>
    .stForm { background-color: #00000; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

with st.form("therapist_form", clear_on_submit=True):
    st.subheader("1. Patient Identification")
    col1, col2 = st.columns(2)
    with col1:
        patient_id = st.text_input("Patient ID *", help="Unique hospital/clinic ID")
    with col2:
        patient_name = st.text_input("Patient Name *")

    st.divider()
    
    st.subheader("2. Core Symptom Tracking (Scale 1-10)")
    c1, c2, c3 = st.columns(3)
    with c1:
        mood = st.slider("Mood (1=Low, 10=High)", 1, 10, 5)
    with c2:
        stress = st.slider("Stress (1=Low, 10=High)", 1, 10, 5)
    with c3:
        anxiety = st.slider("Anxiety (1=Calm, 10=Panic)", 1, 10, 3)

    st.divider()

    st.subheader("3. Biological & Behavioral Factors")
    b1, b2 = st.columns(2)
    with b1:
        sleep = st.selectbox("Sleep Quality", ["Restorative", "Average", "Interrupted", "Insomnia"])
    with b2:
        appetite = st.selectbox("Appetite Change", ["Normal", "Increased", "Decreased", "Highly Irregular"])
    
    social_withdrawal = st.checkbox("Evidence of Social Withdrawal?")
    
    st.divider()

    st.subheader("4. Clinical Assessment & CBT Focus")
    # This part is CRITICAL for the Gemini Bot to be effective
    distortions = st.multiselect(
        "Identified Cognitive Distortions",
        ["Catastrophizing", "All-or-Nothing Thinking", "Overgeneralization", "Mind Reading", "Emotional Reasoning", "Labeling"]
    )
    
    cbt_goal = st.text_input("Primary Goal for this AI session", placeholder="e.g., Challenge work-related anxiety")
    
    notes = st.text_area("Detailed Clinical Observations", height=150, help="Brief the AI on specific events or feelings.")

    submit = st.form_submit_button("Submit Exam")
    # ... (all your existing code up to 'submit = st.form_submit_button(...)')

if submit:
    if not patient_id or not patient_name:
        st.error("⚠️ Error: Patient ID and Name are required.")
    else:
        try:
            # 1. Open Connection
            conn = get_connection()
            if conn:
                cur = conn.cursor()
                
                # 2. Prepare the SQL (Matches the expanded table we discussed)
                query = """
                    INSERT INTO therapist_inputs 
                    (patient_id, patient_name, mood_level, stress_level, anxiety_level, 
                     sleep_quality, appetite, social_withdrawal, distortions, cbt_goal, notes, therapist_id, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                # Convert the multiselect list into a single string for the DB
                distortion_str = ", ".join(distortions)
                
                # Get current therapist ID from session state
                t_id = st.session_state.get("user_id")
                
                # 3. Execute with data tuple
                cur.execute(query, (
                    patient_id, patient_name, mood, stress, anxiety, 
                    sleep, appetite, social_withdrawal, distortion_str, cbt_goal, notes, t_id,
                    datetime.datetime.now()
                ))
                
                # 4. COMMIT the transaction (Very important!)
                conn.commit()
                
                cur.close()
                conn.close()
                
                st.success(f"✅ Data for {patient_name} saved successfully!")
                
                             
        except Exception as e:
            st.error(f"❌ Database Error: {e}")
if st.button("Go to Dashboard"):
    st.switch_page("pages/3_dashboard.py")