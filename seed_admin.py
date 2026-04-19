import psycopg2
from db import hash_password, get_connection

def seed_admin():
    conn = get_connection()
    if not conn:
        print("Failed to connect to database.")
        return
    cur = conn.cursor()
    try:
        username = "admin"
        password = "Password"
        pwd_hash = hash_password(password)
        
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) ON CONFLICT (username) DO NOTHING", (username, pwd_hash, 'admin'))
        conn.commit()
        print(f"Admin user seeded with Super Admin role: {username} / {password}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_admin()
