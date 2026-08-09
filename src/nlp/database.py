# src/nlp/database.py

import os
import sqlite3

# Define absolute paths to ensure it never fails with "unable to open database file"
BASE_DIR = r"C:\Users\darsh\nifty100_analytics"
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "nifty100.db")

def get_connection():
    """
    Creates the data directory if it doesn't exist, then opens 
    and returns a SQLite database connection safely.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
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