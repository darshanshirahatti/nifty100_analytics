# src/analytics/cagr.py

def compute_cagr(start_val, end_val, num_years):
    """
    Computes CAGR using the formula: ((end/start)^(1/n) - 1) * 100
    Handles the 6 strict financial edge cases defined in Sprint 2.
    """
    if num_years < 1:
        return None, "INSUFFICIENT"
        
    if start_val is None or end_val is None:
        return None, "INSUFFICIENT"

    if start_val == 0:
        return None, "ZERO_BASE"

    # Edge Case Handlers
    if start_val > 0 and end_val > 0:
        try:
            val = ((end_val / start_val) ** (1.0 / num_years) - 1) * 100
            return round(val, 2), "NORMAL"
        except Exception:
            return None, "ERROR"
            
    elif start_val > 0 and end_val <= 0:
        return None, "DECLINE_TO_LOSS"
        
    elif start_val < 0 and end_val > 0:
        return None, "TURNAROUND"
        
    elif start_val < 0 and end_val < 0:
        return None, "BOTH_NEGATIVE"
        
    return None, "UNKNOWN"
print("cagr.py loaded successfully")