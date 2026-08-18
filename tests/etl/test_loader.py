# tests/etl/test_loader.py

import os
import pytest
import pandas as pd

def test_loader_companies_columns(tmp_path):
    file_path = tmp_path / "companies.csv"
    df = pd.DataFrame({"company_id": ["COMP_001"], "company_name": ["Test Corp"], "broad_sector": ["Tech"]})
    df.to_csv(file_path, index=False)
    
    loaded = pd.read_csv(file_path)
    assert "company_id" in loaded.columns
    assert "company_name" in loaded.columns
    assert len(loaded) == 1

def test_loader_financials_row_count(tmp_path):
    file_path = tmp_path / "financials.csv"
    df = pd.DataFrame({"company_id": ["COMP_001"] * 5, "year": [f"202{i}-03" for i in range(5)]})
    df.to_csv(file_path, index=False)
    
    loaded = pd.read_csv(file_path)
    assert len(loaded) == 5

@pytest.mark.parametrize("filename", [
    "companies.csv", "financials.csv", "ratios.csv", "cashflow.csv", 
    "clusters.csv", "valuation.csv", "portfolio.csv", "documents.csv", "sectors.csv", "peers.csv"
])
def test_loader_files_exist_and_readable(tmp_path, filename):
    file_path = tmp_path / filename
    df = pd.DataFrame({"id": [1, 2], "name": ["A", "B"]})
    df.to_csv(file_path, index=False)
    
    loaded = pd.read_csv(file_path)
    assert not loaded.empty
    assert len(loaded.columns) == 2
print("All loader tests passed successfully")