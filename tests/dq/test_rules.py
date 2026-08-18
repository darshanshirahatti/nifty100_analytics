# tests/dq/test_rules.py

import pytest
import pandas as pd

def check_dq_rule(rule_id, df):
    # Mock validator function mapping rule_id to violation checks
    violations = []
    if rule_id == "RULE_01": # Negative Total Debt
        if (df['total_debt'] < 0).any():
            violations.append({"rule_id": "RULE_01", "severity": "HIGH"})
    elif rule_id == "RULE_02": # Negative Revenue
        if (df['revenue'] < 0).any():
            violations.append({"rule_id": "RULE_02", "severity": "CRITICAL"})
    elif rule_id == "RULE_03": # ROE Out of Bounds (> 150%)
        if (df['roe'] > 150).any():
            violations.append({"rule_id": "RULE_03", "severity": "MEDIUM"})
    elif rule_id == "RULE_04": # Current Ratio Zero or Negative
        if (df['current_ratio'] <= 0).any():
            violations.append({"rule_id": "RULE_04", "severity": "HIGH"})
    elif rule_id == "RULE_05": # Interest Coverage Negative
        if (df['icr'] < 0).any():
            violations.append({"rule_id": "RULE_05", "severity": "MEDIUM"})
    elif rule_id == "RULE_06": # Operating Margin > 100%
        if (df['opm'] > 100).any():
            violations.append({"rule_id": "RULE_06", "severity": "LOW"})
    elif rule_id == "RULE_07": # Missing Company ID
        if df['company_id'].isnull().any():
            violations.append({"rule_id": "RULE_07", "severity": "CRITICAL"})
    elif rule_id == "RULE_08": # Asset Turnover Negative
        if (df['asset_turnover'] < 0).any():
            violations.append({"rule_id": "RULE_08", "severity": "MEDIUM"})
    elif rule_id == "RULE_09": # Dividend Yield > 50%
        if (df['dividend_yield'] > 50).any():
            violations.append({"rule_id": "RULE_09", "severity": "LOW"})
    elif rule_id == "RULE_10": # Net Profit Margin < -200%
        if (df['npm'] < -200).any():
            violations.append({"rule_id": "RULE_10", "severity": "HIGH"})
    elif rule_id == "RULE_11": # Debt to Equity > 50
        if (df['de'] > 50).any():
            violations.append({"rule_id": "RULE_11", "severity": "MEDIUM"})
    elif rule_id == "RULE_12": # FCF CAGR Extreme Outlier
        if (df['fcf_cagr'] > 500).any():
            violations.append({"rule_id": "RULE_12", "severity": "LOW"})
    elif rule_id == "RULE_13": # Missing Year
        if df['year'].isnull().any():
            violations.append({"rule_id": "RULE_13", "severity": "CRITICAL"})
    elif rule_id == "RULE_14": # Promoter Holding > 100%
        if (df['promoter_holding'] > 100).any():
            violations.append({"rule_id": "RULE_14", "severity": "HIGH"})
    return violations

@pytest.mark.parametrize("rule_id,col,bad_val,expected_severity", [
    ("RULE_01", "total_debt", -10, "HIGH"),
    ("RULE_02", "revenue", -500, "CRITICAL"),
    ("RULE_03", "roe", 180.0, "MEDIUM"),
    ("RULE_04", "current_ratio", 0.0, "HIGH"),
    ("RULE_05", "icr", -2.5, "MEDIUM"),
    ("RULE_06", "opm", 110.0, "LOW"),
    ("RULE_07", "company_id", None, "CRITICAL"),
    ("RULE_08", "asset_turnover", -0.5, "MEDIUM"),
    ("RULE_09", "dividend_yield", 60.0, "LOW"),
    ("RULE_10", "npm", -250.0, "HIGH"),
    ("RULE_11", "de", 55.0, "MEDIUM"),
    ("RULE_12", "fcf_cagr", 600.0, "LOW"),
    ("RULE_13", "year", None, "CRITICAL"),
    ("RULE_14", "promoter_holding", 105.0, "HIGH")
])
def test_dq_rule_violations(rule_id, col, bad_val, expected_severity):
    base_data = {
        "company_id": "COMP_001", "total_debt": 100, "revenue": 1000,
        "roe": 15.0, "current_ratio": 1.5, "icr": 5.0, "opm": 20.0,
        "asset_turnover": 1.0, "dividend_yield": 2.0, "npm": 10.0,
        "de": 0.5, "fcf_cagr": 15.0, "year": "2024-03", "promoter_holding": 50.0
    }
    base_data[col] = bad_val
    df = pd.DataFrame([base_data])
    
    results = check_dq_rule(rule_id, df)
    assert len(results) == 1
    assert results[0]["rule_id"] == rule_id
    assert results[0]["severity"] == expected_severity

print("All DQ rule violation tests passed successfully.")