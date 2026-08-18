import os
import sqlite3

def optimize_database():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(base_dir, "nifty100.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List of tables that contain company_id and/or year columns
    tables = [
        "profitandloss", "balancesheet", "cashflow", 
        "financial_ratios", "stock_prices", "analysis", "valuation"
    ]
    
    print("Applying SQLite query optimisations...")
    for table in tables:
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table}_company_id ON {table}(company_id);")
            print(f"Created index on {table}(company_id)")
        except Exception as e:
            print(f"Skipped company_id index for {table}: {e}")
            
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table}_year ON {table}(year);")
            print(f"Created index on {table}(year)")
            print(f"Created index on {table}(year)")
        except Exception as e:
            print(f"Skipped year index for {table}: {e}")

    conn.commit()
    conn.close()
    print("[Database] Optimization completed successfully.")

if __name__ == "__main__":
    optimize_database()