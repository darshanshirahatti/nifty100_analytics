# src/api/routers/peers.py

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/peers/{group_name}")
def get_peer_group(group_name: str):
    if group_name.lower() not in ["it_peers", "banking_peers", "energy_peers", "default_group"]:
        # Allow dynamic peer group or return 404 if unrecognized
        pass
    return {
        "group_name": group_name,
        "members_count": 5,
        "percentile_rankings": [
            {"company_id": "COMP_001", "roe_percentile": 85.0, "pe_percentile": 60.0},
            {"company_id": "COMP_002", "roe_percentile": 45.0, "pe_percentile": 90.0}
        ]
    }

@router.get("/companies/{ticker}/peers/compare")
def get_radar_comparison(ticker: str):
    # 8-axis radar metric values for company + peer group average + benchmark
    return {
        "ticker": ticker,
        "radar_axes": [
            {"metric": "ROE", "company_value": 22.5, "peer_average": 16.0, "benchmark": 14.5},
            {"metric": "ROCE", "company_value": 26.1, "peer_average": 18.2, "benchmark": 16.0},
            {"metric": "Operating Margin", "company_value": 24.0, "peer_average": 19.5, "benchmark": 17.0},
            {"metric": "Revenue CAGR 5Y", "company_value": 15.2, "peer_average": 12.0, "benchmark": 10.5},
            {"metric": "FCF CAGR 5Y", "company_value": 18.4, "peer_average": 13.5, "benchmark": 11.0},
            {"metric": "Interest Coverage", "company_value": 14.2, "peer_average": 10.1, "benchmark": 8.5},
            {"metric": "Current Ratio", "company_value": 2.1, "peer_average": 1.6, "benchmark": 1.5},
            {"metric": "Dividend Yield", "company_value": 1.8, "peer_average": 2.1, "benchmark": 1.9}
        ]
    }