# 🧠 AI CBT Therapy Portal

A scalable, AI-powered Cognitive Behavioral Therapy (CBT) platform designed to deliver personalized mental health support through role-based access, structured clinical input, and persistent conversational sessions.

---

## 🚀 Key Features

* **Role-Based Navigation**
  Dynamic sidebar that adapts to user roles (Therapist / Patient), ensuring a focused and intuitive experience.

* **Secure Authentication**
  Robust login system with database integration and `bcrypt` password hashing for enhanced security.

* **Clinical Intake System**
  Structured therapist input capturing mood, stress levels, and cognitive distortions to guide AI responses.

* **Persistent AI Conversations**
  AI-driven therapy sessions powered by Google Gemini with full chat history storage and retrieval.

* **Analytics Dashboard**
  Real-time insights into patient progress, mood trends, and identification of high-risk cases.

---

## 🛠️ Setup Instructions

### 1. Prerequisites

Ensure the following are installed:

* Python 3.9+
* PostgreSQL 17

Install required dependencies:

```bash
pip install streamlit psycopg2-binary google-generativeai bcrypt pandas
```

---

### 2. Database Setup

1. Create a PostgreSQL database named:

```
therapy_db
```

2. Run the schema script to initialize tables:

```sql
\i d:/CBT/CBT/schema.sql
```

---

### 3. Seed Therapist Account

Create the default therapist account:

```bash
python seed_admin.py
```

**Default Credentials:**

* Username: `admin`
* Password: `Password`

---

### 4. Run the Application

```bash
streamlit run app.py
```

---

## 🔄 User Workflow

### 👩‍⚕️ Therapist Flow

1. **Login**
   Access the Therapist Login panel.

2. **Clinical Intake**
   Record patient observations including emotional state and cognitive patterns.

3. **Dashboard Monitoring**
   Track patient progress, analyze trends, and identify high-risk individuals.

---

### 🧑‍💻 Patient Flow

1. **Access Portal**
   Enter the assigned **Patient ID** provided by the therapist.

2. **AI Therapy Session**
   Engage in personalized CBT conversations informed by therapist inputs.

3. **Session Continuity**
   Resume previous conversations anytime with saved chat history.

---

## 📂 Project Structure

```
CBT/
│
├── app.py                # Main application & navigation logic
├── db.py                 # Database connection and utilities
├── seed_admin.py         # Script to create therapist account
│
├── pages/
│   ├── 1_input.py        # Clinical Intake Module
│   ├── 2_chat.py         # AI Therapy Chat Interface
│   └── 3_dashboard.py    # Analytics Dashboard
│
└── schema.sql            # Database schema definition
```

---

## 💡 Overview

This platform bridges the gap between traditional therapy and AI by integrating therapist-provided clinical data with real-time conversational intelligence. It ensures personalized, context-aware, and continuous mental health support while maintaining scalability and usability.

