import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_database():
    # Connect to the default 'postgres' database to create the new one
    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Password",
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Create database if not exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'therapy_db'")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE therapy_db")
            print("Database 'therapy_db' created successfully.")
        else:
            print("Database 'therapy_db' already exists.")
            
        cur.close()
        conn.close()
        
        # Now connect to 'therapy_db' and run schema
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Password",
            database="therapy_db"
        )
        cur = conn.cursor()
        with open("schema.sql", "r") as f:
            cur.execute(f.read())
        conn.commit()
        print("Schema applied successfully.")
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_database()
