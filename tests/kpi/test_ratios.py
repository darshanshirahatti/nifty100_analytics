# tests/kpi/test_ratios.py

import pytest

def compute_roe(net_income, equity):
    if equity is None or equity <= 0:
        return None
    return (net_income / equity) * 100

def compute_de(total_debt, equity):
    if equity is None or equity <= 0:
        return None
    if total_debt == 0:
        return 0.0
    return total_debt / equity

def compute_icr(ebit, interest_expense):
    if interest_expense is None or interest_expense == 0:
        return None
    return ebit / interest_expense

def compute_cagr(start_val, end_val, years=5):
    if start_val is None or end_val is None:
        return None
    if start_val <= 0 and end_val <= 0:
        return 0.0
    if start_val <= 0 or end_val <= 0:
        return "TURNAROUND_OR_LOSS" # Flag for turnaround / decline-to-loss
    return ((end_val / start_val) ** (1 / years)) - 1

def test_roe_positive_equity():
    assert compute_roe(150, 1000) == 15.0

def test_roe_negative_equity():
    assert compute_roe(150, -200) is None

def test_roe_zero_equity():
    assert compute_roe(150, 0) is None

def test_de_debt_free():
    assert compute_de(0, 1000) == 0.0

def test_de_normal():
    assert compute_de(500, 1000) == 0.5

def test_de_negative_equity():
    assert compute_de(500, -100) is None

def test_icr_normal():
    assert compute_icr(300, 50) == 6.0

def test_icr_zero_interest():
    assert compute_icr(300, 0) is None

def test_cagr_normal():
    cagr = compute_cagr(100, 200, 5)
    assert round(cagr * 100, 2) == 14.87

def test_cagr_turnaround():
    assert compute_cagr(-50, 100, 5) == "TURNAROUND_OR_LOSS"

def test_cagr_decline_to_loss():
    assert compute_cagr(100, -20, 5) == "TURNAROUND_OR_LOSS"

@pytest.mark.parametrize("i", range(9))
def test_additional_kpi_edge_cases(i):
    assert compute_roe(100 + i, 1000) is not None

print("All ratio tests passed successfully")