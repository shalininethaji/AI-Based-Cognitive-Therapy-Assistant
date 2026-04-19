import psycopg2
from psycopg2 import OperationalError
import bcrypt

def get_connection():
    try:
        return psycopg2.connect(
            host="localhost",
            database="therapy_db",
            user="postgres",
            password="Password"
        )
    except OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None

# --- AUTHENTICATION ---
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(username, password):
    conn = get_connection()
    if not conn: return None
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, password_hash, role, patient_id FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        if result and check_password(password, result[1]):
            return {"id": result[0], "role": result[2], "patient_id": result[3]}
        return None
    finally:
        cur.close()
        conn.close()

def register_user(username, password, role, patient_id=None):
    conn = get_connection()
    if not conn: return False
    cur = conn.cursor()
    try:
        pwd_hash = hash_password(password)
        cur.execute(
            "INSERT INTO users (username, password_hash, role, patient_id) VALUES (%s, %s, %s, %s)",
            (username, pwd_hash, role, patient_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Registration error: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def list_all_therapists():
    conn = get_connection()
    if not conn: return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, username, created_at FROM users WHERE role = 'therapist'")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def list_all_patients():
    # Shows all patients from the users table or inputs
    conn = get_connection()
    if not conn: return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT patient_id, patient_name, therapist_id, created_at FROM therapist_inputs")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def delete_user(user_id):
    conn = get_connection()
    if not conn: return False
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return True
    finally:
        cur.close()
        conn.close()

# --- CHAT HISTORY ---
def save_chat_message(patient_id, role, content):
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO chat_history (patient_id, role, content) VALUES (%s, %s, %s)",
            (patient_id, role, content)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def get_chat_history(patient_id):
    conn = get_connection()
    if not conn: return []
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT role, content FROM chat_history WHERE patient_id = %s ORDER BY created_at ASC",
            (patient_id,)
        )
        return [{"role": row[0], "content": row[1]} for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

def get_patient_context(patient_id):
    conn = get_connection()
    if conn is None:
        return "System error: Unable to connect to clinical records."

    cur = conn.cursor()
    try:
        # UPDATED: Added new columns for a richer AI context
        cur.execute("""
            SELECT mood_level, stress_level, anxiety_level, sleep_quality, 
                   appetite, social_withdrawal, distortions, cbt_goal, notes
            FROM therapist_inputs
            WHERE patient_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (patient_id,))

        data = cur.fetchone()
        
        if data:
            # We structure this clearly so the LLM understands the clinical breakdown
            return f"""
            --- CLINICAL BRIEFING FOR PATIENT {patient_id} ---
            Symptom Scores:
            - Mood: {data[0]}/10
            - Stress: {data[1]}/10
            - Anxiety: {data[2]}/10
            
            Biological/Behavioral:
            - Sleep: {data[3]}
            - Appetite: {data[4]}
            - Social Withdrawal: {'Yes' if data[5] else 'No'}
            
            CBT Specifics:
            - Identified Distortions: {data[6]}
            - Today's Therapeutic Goal: {data[7]}
            
            Therapist's Direct Notes: 
            "{data[8]}"
            ------------------------------------------------
            """
        else:
            return "No previous therapist session recorded. Provide general CBT support."

    except Exception as e:
        return f"Error retrieving patient data: {e}"
    
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()