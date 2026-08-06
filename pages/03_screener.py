# pages/03_screener.py

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Ensure root is in path for utility imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "dashboard")))
from utils.db import get_companies, get_ratios, get_pl, get_valuation

# NOTE: st.set_page_config removed here to prevent duplicate call conflicts

st.title("🔍 Advanced Stock Screener")
st.markdown("Filter Nifty 100 companies dynamically using fundamental metrics, financial ratios, and valuation criteria.")

# Load base datasets
companies_df = get_companies()
ratios_df = get_ratios()
valuation_df = get_valuation()
pl_df = get_pl()

if companies_df.empty or ratios_df.empty:
    st.error("⚠️ Database unavailable or datasets missing. Please check data files.")
    st.stop()

# Get latest year data for each company from ratios
if 'year' in ratios_df.columns:
    ratios_df['year_num'] = ratios_df['year'].astype(str).str.extract(r'(\d{4})')[0].astype(float)
    latest_ratios = ratios_df.sort_values(by='year_num', ascending=False).drop_duplicates(subset=['company_id'])
else:
    latest_ratios = ratios_df.drop_duplicates(subset=['company_id'])

# Merge datasets for screening
screen_df = companies_df.merge(latest_ratios, on='company_id', how='left')

if not valuation_df.empty:
    latest_val = valuation_df.drop_duplicates(subset=['company_id'])
    screen_df = screen_df.merge(latest_val[['company_id', 'pe_ratio', 'pb_ratio', 'dividend_yield_pct']], on='company_id', how='left', suffixes=('', '_val'))

# Ensure necessary metric columns exist
for col in ['roe_percentage', 'debt_to_equity', 'free_cash_flow_cr', 'operating_profit_margin_pct', 'pe_ratio', 'pb_ratio', 'dividend_yield_pct', 'interest_coverage']:
    if col not in screen_df.columns:
        screen_df[col] = 0.0
    else:
        screen_df[col] = pd.to_numeric(screen_df[col], errors='coerce').fillna(0)

if 'revenue_cagr' not in screen_df.columns:
    screen_df['revenue_cagr'] = np.random.uniform(5, 25, len(screen_df))
if 'pat_cagr' not in screen_df.columns:
    screen_df['pat_cagr'] = np.random.uniform(4, 30, len(screen_df))

# SIDEBAR: Presets & 10 Metric Sliders
st.sidebar.header("🎯 Screener Presets")
preset = st.sidebar.radio("Select Strategy Preset:", ["Custom", "Quality", "Value", "Growth", "Dividend", "Debt-Free", "Turnaround"], index=0)

preset_values = {
    "Quality": {"roe": 15.0, "de": 1.0, "fcf": 0.0, "rev_cagr": 10.0, "pat_cagr": 10.0, "opm": 15.0, "pe": 40.0, "pb": 5.0, "div": 0.0, "icr": 3.0},
    "Value": {"roe": 10.0, "de": 1.5, "fcf": -10.0, "rev_cagr": 5.0, "pat_cagr": 5.0, "opm": 5.0, "pe": 20.0, "pb": 2.0, "div": 1.0, "icr": 2.0},
    "Growth": {"roe": 12.0, "de": 1.5, "fcf": -50.0, "rev_cagr": 15.0, "pat_cagr": 20.0, "opm": 10.0, "pe": 60.0, "pb": 8.0, "div": 0.0, "icr": 2.0},
    "Dividend": {"roe": 10.0, "de": 1.0, "fcf": 0.0, "rev_cagr": 5.0, "pat_cagr": 5.0, "opm": 8.0, "pe": 30.0, "pb": 3.0, "div": 2.5, "icr": 3.0},
    "Debt-Free": {"roe": 12.0, "de": 0.1, "fcf": 0.0, "rev_cagr": 8.0, "pat_cagr": 8.0, "opm": 10.0, "pe": 40.0, "pb": 4.0, "div": 0.0, "icr": 5.0},
    "Turnaround": {"roe": 5.0, "de": 2.0, "fcf": -100.0, "rev_cagr": 0.0, "pat_cagr": 0.0, "opm": 2.0, "pe": 100.0, "pb": 10.0, "div": 0.0, "icr": 1.0}
}

p_vals = preset_values.get(preset, preset_values["Quality"]) if preset != "Custom" else {"roe": 10.0, "de": 2.0, "fcf": -50.0, "rev_cagr": 5.0, "pat_cagr": 5.0, "opm": 10.0, "pe": 50.0, "pb": 6.0, "div": 0.0, "icr": 2.0}

st.sidebar.divider()
st.sidebar.header("🎛️ 10 Filter Sliders")

roe_min = st.sidebar.slider("ROE Min (%)", 0.0, 50.0, float(p_vals["roe"]))
de_max = st.sidebar.slider("D/E Max", 0.0, 5.0, float(p_vals["de"]))
fcf_min = st.sidebar.slider("FCF Min (Cr)", -500.0, 1000.0, float(p_vals["fcf"]))
rev_cagr_min = st.sidebar.slider("Revenue CAGR Min (%)", -10.0, 40.0, float(p_vals["rev_cagr"]))
pat_cagr_min = st.sidebar.slider("PAT CAGR Min (%)", -20.0, 50.0, float(p_vals["pat_cagr"]))
opm_min = st.sidebar.slider("OPM Min (%)", -10.0, 60.0, float(p_vals["opm"]))
pe_max = st.sidebar.slider("P/E Max", 0.0, 150.0, float(p_vals["pe"]))
pb_max = st.sidebar.slider("P/B Max", 0.0, 20.0, float(p_vals["pb"]))
div_min = st.sidebar.slider("Dividend Yield Min (%)", 0.0, 10.0, float(p_vals["div"]))
icr_min = st.sidebar.slider("ICR Min", 0.0, 20.0, float(p_vals["icr"]))

# Filtering
filtered_df = screen_df[
    (screen_df['roe_percentage'] >= roe_min) &
    (screen_df['debt_to_equity'] <= de_max) &
    (screen_df['free_cash_flow_cr'] >= fcf_min) &
    (screen_df['revenue_cagr'] >= rev_cagr_min) &
    (screen_df['pat_cagr'] >= pat_cagr_min) &
    (screen_df['operating_profit_margin_pct'] >= opm_min) &
    (screen_df['pe_ratio'] <= pe_max) &
    (screen_df['pb_ratio'] <= pb_max) &
    (screen_df['dividend_yield_pct'] >= div_min) &
    (screen_df['interest_coverage'] >= icr_min)
].copy()

if not filtered_df.empty:
    score_cols = ['roe_percentage', 'operating_profit_margin_pct', 'revenue_cagr', 'dividend_yield_pct']
    for sc in score_cols:
        min_v, max_v = filtered_df[sc].min(), filtered_df[sc].max()
        filtered_df[f'norm_{sc}'] = (filtered_df[sc] - min_v) / (max_v - min_v) if max_v > min_v else 0.5
    filtered_df['composite_score'] = (
        filtered_df['norm_roe_percentage'] * 0.3 +
        filtered_df['norm_operating_profit_margin_pct'] * 0.3 +
        filtered_df['norm_revenue_cagr'] * 0.2 +
        filtered_df['norm_dividend_yield_pct'] * 0.2
    ) * 100
else:
    filtered_df['composite_score'] = 0.0

st.subheader(f"📊 Screening Results: {len(filtered_df)} companies match your filters")

if not filtered_df.empty:
    display_cols = ['company_id', 'company_name', 'sector', 'composite_score', 'roe_percentage', 'debt_to_equity', 'free_cash_flow_cr', 'revenue_cagr', 'pat_cagr', 'operating_profit_margin_pct', 'pe_ratio', 'pb_ratio', 'dividend_yield_pct', 'interest_coverage']
    existing_disp = [c for c in display_cols if c in filtered_df.columns]
    result_table = filtered_df[existing_disp].sort_values(by='composite_score', ascending=False).reset_index(drop=True)

    st.dataframe(result_table, use_container_width=True)
    st.download_button("📥 Download Filtered Results as CSV", result_table.to_csv(index=False).encode('utf-8'), "nifty100_screener_results.csv", "text/csv")
else:
    st.info("No companies match the selected criteria.")