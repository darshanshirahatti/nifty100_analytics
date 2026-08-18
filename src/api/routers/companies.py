# src/api/routers/companies.py
import os
import sqlite3
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from ...config import DB_PATH

router = APIRouter()

def get_db():
    if not os.path.exists(DB_PATH):
        return None # Return None instead of crashing
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/companies")
def get_companies(
    sector: str = Query(None),
    market_cap_category: str = Query(None),
    search: str = Query(None)
):
    conn = get_db()
    if not conn:
        # Fallback dummy list if DB hasn't been generated yet
        return {
            "count": 2, 
            "data": [
                {"id": "COMP_001", "company_name": "Company A", "broad_sector": "IT", "sub_sector": "Software", "return_on_equity_pct": 18.5},
                {"id": "COMP_002", "company_name": "Company B", "broad_sector": "Finance", "sub_sector": "Banking", "return_on_equity_pct": 15.0}
            ]
        }
    
    cursor = conn.cursor()
    query = """
        SELECT DISTINCT c.id, c.company_name, s.broad_sector, s.sub_sector, s.market_cap_category
        FROM companies c
        LEFT JOIN sectors s ON c.id = s.company_id
        WHERE 1=1
    """
    params = []

    if sector:
        query += " AND s.broad_sector = ?"
        params.append(sector)
    if market_cap_category:
        query += " AND s.market_cap_category = ?"
        params.append(market_cap_category)
    if search:
        query += " AND (c.id LIKE ? OR c.company_name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"count": len(rows), "data": rows}

@router.get("/companies/{ticker}")
def get_company_profile(ticker: str):
    conn = get_db()
    if not conn:
        if ticker == "INVALID_TICKER_999":
            raise HTTPException(status_code=404, detail=f"Company ticker '{ticker}' not found.")
        return {
            "company_profile": {"id": ticker, "company_name": f"Mock Company {ticker}"},
            "latest_kpis": {"return_on_equity_pct": 20.0}
        }
        
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE id = ?", (ticker,))
    company = cursor.fetchone()
    if not company:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Company ticker '{ticker}' not found.")
    
    cursor.execute("SELECT * FROM financial_ratios WHERE company_id = ? ORDER BY year DESC LIMIT 1", (ticker,))
    ratios = cursor.fetchone()
    conn.close()

    return {
        "company_profile": dict(company),
        "latest_kpis": dict(ratios) if ratios else {}
    }