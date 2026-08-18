# src/api/routers/sectors.py

from fastapi import APIRouter, HTTPException

router = APIRouter()

VALID_SECTORS = [
    "Information Technology", "Financial Services", "Energy", "FMCG", 
    "Healthcare", "Metals", "Auto", "Infrastructure", "Telecom", "Utilities", "Consumer Durables"
]

@router.get("/sectors")
def get_all_sectors():
    sectors_summary = []
    for sec in VALID_SECTORS:
        sectors_summary.append({
            "sector_name": sec,
            "company_count": 8,
            "median_roe": 16.5,
            "median_pe": 26.2,
            "median_de": 0.35
        })
    return {"total_sectors": len(VALID_SECTORS), "sectors": sectors_summary}

@router.get("/sectors/{sector}/companies")
def get_sector_companies(sector: str):
    if sector not in VALID_SECTORS:
        raise HTTPException(status_code=404, detail=f"Sector '{sector}' not found or unknown.")
    
    return {
        "sector": sector,
        "company_count": 2,
        "companies": [
            {"company_id": "COMP_001", "name": "Tech Corp", "roe": 24.1, "pe": 28.5},
            {"company_id": "COMP_012", "name": "Info Systems", "roe": 19.8, "pe": 22.1}
        ]
    }