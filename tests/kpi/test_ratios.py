# tests/kpi/test_ratios.py
import pytest
from src.analytics.ratios import compute_npm, compute_roe, compute_de

def test_profitability_npm():
    assert compute_npm(10, 100) == 10.0
    assert compute_npm(10, 0) is None

def test_profitability_roe():
    # Regular Case
    assert compute_roe(20, 10, 90) == 20.0
    # Negative Equity Case
    assert compute_roe(20, -50, 10) is None

def test_leverage_de():
    de_val, warning = compute_de(50, 10, 90)
    assert de_val == 0.5
    assert warning is False