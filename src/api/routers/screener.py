# src/api/routers/screener.py

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/screener")
def run_screener(
    min_roe: float = Query(None, description="Minimum ROE %"),
    max_de: float = Query(None, description="Maximum Debt-to-Equity"),
    min_fcf: float = Query(None, description="Minimum FCF CAGR"),
    sector: str = Query(None),
    min_rev_cagr_5yr: float = Query(None),
    min_pat_cagr_5yr: float = Query(None),
    max_pe: float = Query(None)
):
    # Parameter validation returning HTTP 400 for invalid ranges
    if min_roe is not None and min_roe < -100:
        raise HTTPException(status_code=400, detail="Invalid parameter: min_roe cannot be less than -100%")
    if max_de is not None and max_de < 0:
        raise HTTPException(status_code=400, detail="Invalid parameter: max_de cannot be negative.")
    if max_pe is not None and max_pe < 0:
        raise HTTPException(status_code=400, detail="Invalid parameter: max_pe cannot be negative.")

    # Mock filtered results matching query criteria
    return {
        "filters_applied": {
            "min_roe": min_roe, "max_de": max_de, "min_fcf": min_fcf, 
            "sector": sector, "max_pe": max_pe
        },
        "matched_count": 2,
        "results": [
            {"company_id": "COMP_001", "roe_pct": 22.5, "debt_to_equity": 0.2, "pe": 24.1},
            {"company_id": "COMP_045", "roe_pct": 25.0, "debt_to_equity": 0.1, "pe": 21.5}
        ]
    }