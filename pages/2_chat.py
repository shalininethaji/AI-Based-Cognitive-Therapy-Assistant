import streamlit as st
import google.generativeai as genai
from db import get_patient_context, get_chat_history, save_chat_message

# ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="AI Therapy Session", page_icon="🧘")

# ---------------- SECURITY CHECK ----------------
if st.session_state.get("role") != "patient":
    st.error("Unauthorized access")
    st.stop()

patient_id = st.session_state.get("patient_id")

if not patient_id:
    st.error("Patient session not found. Please login again.")
    st.stop()

st.title("🧘 Personal CBT Session")

# ---------------- GEMINI CONFIG ----------------
genai.configure("GEMINI_API_KEY")

# ---------------- LOAD PATIENT DATA ----------------
with st.spinner("Loading your therapy profile..."):
    clinical_context = get_patient_context(patient_id)

if not clinical_context:
    st.error("Patient data not found. Please contact your therapist.")
    st.stop()

# ---------------- SYSTEM PROMPT ----------------
system_instruction = f"""
You are a professional CBT AI therapist.

Patient Clinical Data:
{clinical_context}

Instructions:
- Start the session by saying something like: "Hello! I've reviewed the notes from your recent exam. I see we're focusing on [Goal] today. How are you feeling right now?" 
- Use the 'Identified Distortions' to guide your questioning. 
- Be empathetic but stay focused on the CBT Goal. 
- Focus on the CBT goal provided by the therapist.
- Ask reflective CBT-style questions.
- Keep responses concise (2-3 sentences).
"""

# ---------------- MODEL INIT ----------------
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction
)

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    # Load from database
    st.session_state.messages = get_chat_history(patient_id)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------
if prompt := st.chat_input("How are you feeling today?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save user message to DB
    save_chat_message(patient_id, "user", prompt)

    try:
        # Prepare history for Gemini
        history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ]

        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)

        with st.chat_message("assistant"):
            st.markdown(response.text)

        # Save assistant message to DB
        save_chat_message(patient_id, "assistant", response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )

    except Exception as e:
        st.error(f"AI Error: {e}")