# tests/api/test_health.py

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint_success():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "uptime_seconds" in data
    
    db_counts = data.get("db_row_counts", {})
    expected_tables = [
        "companies", "financials", "ratios", "cashflow", 
        "clusters", "valuation", "portfolio", "documents", "sectors", "peers"
    ]
    for table in expected_tables:
        assert table in db_counts

print("All health endpoint tests passed successfully.")