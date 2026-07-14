# src/analytics/ratios.py

def compute_npm(net_profit, sales):
    """NPM: (Net Profit / Sales) * 100. Return None if sales == 0."""
    if not sales or sales == 0:
        return None
    return (net_profit / sales) * 100

def compute_opm_crosscheck(operating_profit, sales, reported_opm):
    """OPM: (Operating Profit / Sales) * 100. Crosscheck with reported OPM."""
    if not sales or sales == 0:
        return None, False
    computed_opm = (operating_profit / sales) * 100
    mismatch = abs(computed_opm - reported_opm) > 1.0 if reported_opm is not None else False
    return computed_opm, mismatch

def compute_roe(net_profit, equity_capital, reserves):
    """ROE: (Net Profit / (Equity Capital + Reserves)) * 100. Return None if net worth <= 0."""
    net_worth = (equity_capital or 0) + (reserves or 0)
    if net_worth <= 0:
        return None
    return (net_profit / net_worth) * 100

def compute_roce(ebit, equity, reserves, borrowings):
    """ROCE: (EBIT / (Equity + Reserves + Borrowings)) * 100. Return None if capital employed <= 0."""
    capital_employed = (equity or 0) + (reserves or 0) + (borrowings or 0)
    if capital_employed <= 0:
        return None
    return (ebit / capital_employed) * 100

def compute_roa(net_profit, total_assets):
    """ROA: (Net Profit / Total Assets) * 100. Return None if total_assets == 0."""
    if not total_assets or total_assets == 0:
        return None
    return (net_profit / total_assets) * 100

def compute_de(borrowings, equity_capital, reserves, is_financial=False):
    """D/E: Borrowings / (Equity + Reserves). Return 0 if borrowings == 0."""
    if not borrowings or borrowings == 0:
        return 0.0, False
    net_worth = (equity_capital or 0) + (reserves or 0)
    if net_worth <= 0:
        return None, False
    de_val = borrowings / net_worth
    high_leverage = de_val > 5.0 and not is_financial
    return de_val, high_leverage

def compute_icr(operating_profit, other_income, interest):
    """ICR: (Operating Profit + Other Income) / Interest. Return None if interest == 0 (Debt Free)."""
    if not interest or interest == 0:
        return None, "Debt Free", False
    numerator = (operating_profit or 0) + (other_income or 0)
    icr_val = numerator / interest
    warning = icr_val < 1.5
    return icr_val, None, warning

def compute_net_debt(borrowings, investments):
    """Net Debt: Borrowings - Investments."""
    return (borrowings or 0) - (investments or 0)

def compute_asset_turnover(sales, total_assets):
    """Asset Turnover: Sales / Total Assets."""
    if not total_assets or total_assets == 0:
        return None
    return sales / total_assets
print("ratios.py loaded successfully")