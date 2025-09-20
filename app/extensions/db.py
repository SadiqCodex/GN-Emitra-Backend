import psycopg2
import os

def get_db_connection():
    """Connect to Postgres database using DATABASE_URL"""
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

def init_db():
    """Create tables if they do not exist"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            name TEXT,
            city TEXT,
            rating INT,
            comment TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
