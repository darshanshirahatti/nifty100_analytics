# tests/kpi/test_cagr.py
import pytest
from src.analytics.cagr import compute_cagr

def test_cagr_normal():
    val, flag = compute_cagr(100, 144, 2)
    assert val == 20.0
    assert flag == "NORMAL"

def test_cagr_turnaround():
    val, flag = compute_cagr(-50, 100, 5)
    assert val is None
    assert flag == "TURNAROUND"

def test_cagr_loss():
    val, flag = compute_cagr(100, -20, 3)
    assert val is None
    assert flag == "DECLINE_TO_LOSS"
print("test_cagr.py loaded successfully")