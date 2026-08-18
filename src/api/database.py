import sqlite3
import os
from ..config import DB_PATH

def get_db():
    """Get database connection using shared config path."""
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    # Check if 'companies' table exists
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='companies';")
    if not cursor.fetchone():
        conn.close()
        return None
    return conn

print("Database connection utility loaded successfully.")