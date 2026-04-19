import streamlit as st
import pandas as pd
from db import get_connection


# block non-therapists
if st.session_state.get("role") != "therapist":
    st.error("Unauthorized access")
    st.stop()

# st.set_page_config(page_title="Therapist Dashboard", page_icon="📊")

st.title("📊 Therapist Dashboard")

# ---------- DATABASE FETCH ----------
conn = get_connection()
t_id = st.session_state.get("user_id")

# Filter data by therapist_id
query = "SELECT * FROM therapist_inputs WHERE therapist_id = %s ORDER BY created_at DESC"
df = pd.read_sql(query, conn, params=(t_id,))
conn.close()

if df.empty:
    st.warning("No patient records found.")
    st.stop()

# ---------- TOP METRICS ----------
st.subheader("📈 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", df["patient_id"].nunique())
col2.metric("Avg Mood", round(df["mood_level"].mean(), 2))
col3.metric("Avg Stress", round(df["stress_level"].mean(), 2))
col4.metric("Avg Anxiety", round(df["anxiety_level"].mean(), 2))

st.divider()
sleep_counts = df["sleep_quality"].value_counts()
st.bar_chart(sleep_counts)
# ---------- MOOD TREND ----------
st.subheader("📈 Mood Trend Over Time")

trend_df = df.sort_values("created_at")
st.line_chart(trend_df.set_index("created_at")[["mood_level"]])

st.divider()

# ---------- RECENT PATIENTS ----------
st.subheader("🗂 Recent Sessions")

st.dataframe(
    df[["patient_id", "patient_name", "mood_level", "stress_level", "anxiety_level", "created_at"]],
    use_container_width=True
)

st.divider()

# ---------- PATIENT SEARCH ----------
st.subheader("🔎 Search Patient")

search_id = st.text_input("Enter Patient ID")

if search_id:
    result = df[df["patient_id"] == search_id]
    if not result.empty:
        st.success("Patient Found")
        st.dataframe(result)
    else:
        st.error("No patient found with this ID.")
st.subheader("🚨 High Risk Patients (Anxiety > 8)")

high_risk = df[df["anxiety_level"] > 8]

if not high_risk.empty:
    st.dataframe(high_risk)
else:
    st.success("No high risk patients currently.")