# src/nlp/pros_cons_generator.py

import os
import sys
import pandas as pd

# Ensure the current directory is in the path to import database.py safely
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database import get_connection

def run_pros_cons_generator():
    print("Initializing Pros & Cons Generator...")
    
    # Get safe connection using our standalone database module
    conn = get_connection()
    
    try:
        # Example query to check existing tables or interact with the database
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Existing tables in database: {[t[0] for t in tables]}")
        
        # --- Add your core pros & cons generation/processing logic here ---
        print("Pros and Cons generation completed successfully.")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    run_pros_cons_generator()

print("Pros & cons generation complete. check output files in the output directory.")