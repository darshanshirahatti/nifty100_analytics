# src/analytics/populate_ratios.py

import os
import sqlite3
import pandas as pd
from ratios import *
from cagr import compute_cagr
from cashflow_kpis import compute_fcf, classify_capital_allocation, classify_capex_intensity

# Robust directory-agnostic path system
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "nifty100.db")
LOG_PATH = os.path.join(BASE_DIR, "output", "ratio_edge_cases.log")
CSV_PATH = os.path.join(BASE_DIR, "output", "capital_allocation.csv")

def recreate_financial_ratios_table(conn):
    """
    Guarantees the SQL schema perfectly matches the specifications.
    Drops the existing table and recreates it with the correct fields.
    """
    cursor = conn.cursor()
    print("🧹 Dropping and recreating table 'financial_ratios' with correct schema...")
    cursor.execute("DROP TABLE IF EXISTS financial_ratios;")
    cursor.execute("""
    CREATE TABLE financial_ratios (
        company_id TEXT,
        year TEXT,
        net_profit_margin_pct REAL,
        operating_profit_margin_pct REAL,
        return_on_equity_pct REAL,
        debt_to_equity REAL,
        interest_coverage REAL,
        asset_turnover REAL,
        free_cash_flow_cr REAL,
        capex_cr REAL,
        earnings_per_share REAL,
        book_value_per_share REAL,
        dividend_payout_ratio_pct REAL,
        total_debt_cr REAL,
        cash_from_operations_cr REAL,
        revenue_cagr_5yr REAL,
        pat_cagr_5yr REAL,
        eps_cagr_5yr REAL,
        composite_quality_score REAL,
        PRIMARY KEY (company_id, year)
    );
    """)
    conn.commit()

def run_analytics_engine():
    os.makedirs(os.path.join(BASE_DIR, "output"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Recreate table to heal schema discrepancies
    recreate_financial_ratios_table(conn)
    
    # 2. Load raw data safely
    companies = pd.read_sql_query("SELECT id, roce_percentage, roe_percentage FROM companies", conn)
    p_and_l = pd.read_sql_query("SELECT * FROM profitandloss", conn)
    balance_sheet = pd.read_sql_query("SELECT * FROM balancesheet", conn)
    cash_flow = pd.read_sql_query("SELECT * FROM cashflow", conn)
    
    # Fallback/Safe mappings for Sectors
    try:
        sectors = pd.read_sql_query("SELECT company_id, broad_sector FROM sectors", conn)
    except Exception:
        sectors = pd.DataFrame(columns=["company_id", "broad_sector"])

    financial_sector_companies = set(sectors[sectors['broad_sector'].str.upper() == 'FINANCIALS']['company_id'])

    records_to_insert = []
    allocation_patterns = []
    edge_cases = []

    # Map P&L records
    for _, pl in p_and_l.iterrows():
        comp_id = pl['company_id']
        year = pl['year']
        is_fin = comp_id in financial_sector_companies

        # Fetch matching BS and CF rows safely
        bs = balance_sheet[(balance_sheet['company_id'] == comp_id) & (balance_sheet['year'] == year)]
        cf = cash_flow[(cash_flow['company_id'] == comp_id) & (cash_flow['year'] == year)]

        # Determine structural presence safely without Series truth-checks
        has_bs = not bs.empty
        has_cf = not cf.empty

        bs_row = bs.iloc[0] if has_bs else {}
        cf_row = cf.iloc[0] if has_cf else {}

        # 1. Profitability Ratios
        npm = compute_npm(pl.get('net_profit', 0), pl.get('sales', 0))
        opm, _ = compute_opm_crosscheck(pl.get('operating_profit', 0), pl.get('sales', 0), pl.get('opm_percentage', 0))
        
        equity_cap = bs_row.get('equity_capital', 0) if has_bs else 0
        reserves = bs_row.get('reserves', 0) if has_bs else 0
        borrowings = bs_row.get('borrowings', 0) if has_bs else 0
        total_assets = bs_row.get('total_assets', 0) if has_bs else 0
        investments = bs_row.get('investments', 0) if has_bs else 0

        roe = compute_roe(pl.get('net_profit', 0), equity_cap, reserves)
        
        ebit = (pl.get('operating_profit', 0) or 0) + (pl.get('other_income', 0) or 0)
        roce = compute_roce(ebit, equity_cap, reserves, borrowings)
        roa = compute_roa(pl.get('net_profit', 0), total_assets)

        # 2. Leverage & Efficiency Ratios
        de, high_lev = compute_de(borrowings, equity_cap, reserves, is_fin)
        icr, icr_label, icr_warn = compute_icr(pl.get('operating_profit', 0), pl.get('other_income', 0), pl.get('interest', 0))
        net_debt = compute_net_debt(borrowings, investments)
        asset_turnover = compute_asset_turnover(pl.get('sales', 0), total_assets)

        # 3. Cash Flow KPIs & Allocations
        cfo = cf_row.get('operating_activity', 0) if has_cf else 0
        cfi = cf_row.get('investing_activity', 0) if has_cf else 0
        cff = cf_row.get('financing_activity', 0) if has_cf else 0

        fcf = compute_fcf(cfo, cfi)
        capex_int, capex_label = classify_capex_intensity(cfi, pl.get('sales', 0))
        
        patt, patt_label = classify_capital_allocation(cfo, cfi, cff, pl.get('net_profit', 0))

        allocation_patterns.append({
            "company_id": comp_id, "year": year,
            "cfo_sign": patt[0], "cfi_sign": patt[1], "cff_sign": patt[2],
            "pattern_label": patt_label
        })

        # 4. Multi-Year CAGR Calculation (e.g. 5-Year Revenue growth)
        try:
            curr_yr_int = int(year.split('-')[0])
            prev_yr_str = f"{curr_yr_int - 5}-03"
            prev_pl = p_and_l[(p_and_l['company_id'] == comp_id) & (p_and_l['year'] == prev_yr_str)]
            rev_start = prev_pl.iloc[0]['sales'] if not prev_pl.empty else None
        except Exception:
            rev_start = None

        rev_cagr_5y, cagr_flag = compute_cagr(rev_start, pl.get('sales', 0), 5)

        # Build data row matching schema columns exactly
        records_to_insert.append({
            "company_id": comp_id,
            "year": year,
            "net_profit_margin_pct": npm,
            "operating_profit_margin_pct": opm,
            "return_on_equity_pct": roe,
            "debt_to_equity": de,
            "interest_coverage": icr,
            "asset_turnover": asset_turnover,
            "free_cash_flow_cr": fcf / 10000000.0 if has_cf else None,  # Convert standard FCF to Cr
            "capex_cr": abs(cfi) / 10000000.0 if has_cf else None,       # Convert standard CapEx to Cr
            "earnings_per_share": pl.get('eps', None),
            "book_value_per_share": None, 
            "dividend_payout_ratio_pct": pl.get('dividend_payout', None),
            "total_debt_cr": borrowings / 10000000.0 if has_bs else None,
            "cash_from_operations_cr": cfo / 10000000.0 if has_cf else None,
            "revenue_cagr_5yr": rev_cagr_5y,
            "pat_cagr_5yr": None,
            "eps_cagr_5yr": None,
            "composite_quality_score": 1.0 if (not icr_warn and not high_lev) else 0.0
        })

        # Anomaly Logging
        comp_meta = companies[companies['id'] == comp_id]
        if not comp_meta.empty and roe:
            reported_roe = comp_meta.iloc[0]['roe_percentage']
            if reported_roe and abs(roe - reported_roe) > 5.0:
                edge_cases.append(f"[ROE Anomaly] {comp_id} Year {year}: Computed {roe:.2f}% vs Reported {reported_roe}% | Category: Source discrepancy\n")

    # Save Edge Cases Log File
    with open(LOG_PATH, "w") as lf:
        lf.writelines(edge_cases)

    # Save Capital Allocation Patterns CSV File
    pd.DataFrame(allocation_patterns).to_csv(CSV_PATH, index=False)

    # Convert records list to Pandas DataFrame
    df_db = pd.DataFrame(records_to_insert)

    # Populate final SQL ratios table
    df_db.to_sql("financial_ratios", conn, if_exists="append", index=False)
    conn.commit()
    
    cursor = conn.cursor()
    total_rows = cursor.execute("SELECT COUNT(*) FROM financial_ratios").fetchone()[0]
    conn.close()

    print(f"📊 Ratio Engine successfully populated {total_rows} rows into 'financial_ratios'!")

if __name__ == "__main__":
    run_analytics_engine()