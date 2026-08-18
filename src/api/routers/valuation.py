# src/api/routers/valuation.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/market-cap/{ticker}")
def get_historical_valuation(ticker: str):
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    historical_data = []
    for y in years:
        historical_data.append({
            "year": str(y),
            "pe_ratio": 22.5 + (y - 2019) * 1.2,
            "pb_ratio": 4.1 + (y - 2019) * 0.3,
            "ev_ebitda": 16.2 + (y - 2019) * 0.5,
            "dividend_yield_pct": 1.5
        })
    return {
        "ticker": ticker,
        "valuation_history": historical_data
    }