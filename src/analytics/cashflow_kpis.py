# src/analytics/cashflow_kpis.py

def compute_fcf(operating_activity, investing_activity):
    """FCF: Operating Activity + Investing Activity (usually negative CFI acts as capital expenditure)"""
    return (operating_activity or 0) + (investing_activity or 0)

def compute_cfo_quality(cfo, pat):
    """CFO Quality Score: CFO / PAT. Return None if PAT == 0."""
    if not pat or pat == 0:
        return None
    return cfo / pat

def classify_capex_intensity(investing_activity, sales):
    """CapEx Intensity: (abs(Investing Activity) / Sales) * 100"""
    if not sales or sales == 0:
        return None, "Unknown"
    intensity = (abs(investing_activity or 0) / sales) * 100
    if intensity < 3.0:
        label = "Asset Light"
    elif 3.0 <= intensity <= 8.0:
        label = "Moderate"
    else:
        label = "Capital Intensive"
    return intensity, label

def classify_capital_allocation(cfo, cfi, cff, pat=0):
    """
    Classifies capital allocation patterns based on signs of (CFO, CFI, CFF)
    """
    s_cfo = "+" if (cfo or 0) >= 0 else "-"
    s_cfi = "+" if (cfi or 0) >= 0 else "-"
    s_cff = "+" if (cff or 0) >= 0 else "-"
    
    pattern = (s_cfo, s_cfi, s_cff)
    
    # Classifications
    if pattern == ("+", "-", "-"):
        # Check high shareholder returns subclass
        if pat > 0 and (cfo / pat) > 1.2:
            return pattern, "Shareholder Returns"
        return pattern, "Reinvestor"
    elif pattern == ("+", "+", "-"):
        return pattern, "Liquidating Assets"
    elif pattern == ("-", "+", "+"):
        return pattern, "Distress Signal"
    elif pattern == ("-", "-", "+"):
        return pattern, "Growth Funded by Debt"
    elif pattern == ("+", "+", "+"):
        return pattern, "Cash Accumulator"
    elif pattern == ("-", "-", "-"):
        return pattern, "Pre-Revenue"
    elif pattern == ("+", "-", "+"):
        return pattern, "Mixed"
    else:
        return pattern, "Undefined"
print("cashflow.py loaded successfully")