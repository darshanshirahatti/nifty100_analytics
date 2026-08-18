# tests/api/test_screener.py

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_screener_valid_filter():
    response = client.get("/api/v1/screener?min_roe=15.0")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    for item in data["results"]:
        if "roe_pct" in item:
            assert item["roe_pct"] >= 15.0

def test_screener_invalid_parameter_returns_400():
    # Passing an impossible min_roe or invalid range
    response = client.get("/api/v1/screener?min_roe=-150.0")
    assert response.status_code == 400
    assert "invalid" in response.json()["detail"].lower()

print("All screener API tests Passed Successfully.")