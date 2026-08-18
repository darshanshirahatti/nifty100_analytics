

import time
import sqlite3
from fastapi import APIRouter
from ...config import DB_PATH

router = APIRouter()
START_TIME = time.time()

@router.get("/health")
def health_check():
    tables = [
        "companies", "financials", "ratios", "cashflow", 
        "clusters", "valuation", "portfolio", "documents", "sectors", "peers"
    ]
    
    row_counts = {}
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_counts[table] = cursor.fetchone()[0]
            except sqlite3.OperationalError:
                row_counts[table] = 0 # Table may not be initialized yet
        conn.close()
    except Exception as e:
        row_counts["db_error"] = str(e)

    uptime = int(time.time() - START_TIME)
    
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": uptime,
        "db_row_counts": row_counts
    }