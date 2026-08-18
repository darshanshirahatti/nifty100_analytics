# src/nlp/database.py

import os
import sqlite3
from ..config import DB_PATH

def get_connection():
    """
    Creates the data directory if it doesn't exist, then opens 
    and returns a SQLite database connection safely.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.OperationalError as e:
        print(f"Error opening database at {DB_PATH}: {e}")
        raise

if __name__ == "__main__":
    conn = get_connection()
    print("Successfully connected to SQLite database at:", DB_PATH)
    conn.close()