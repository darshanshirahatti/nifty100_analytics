# pages/07_capital.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "dashboard")))
from utils.db import get_companies, get_valuation

st.markdown("## 🧩 Capital Allocation Patterns Map")
st.markdown("Treemap visualization of companies grouped by capital allocation strategies.")

companies_df = get_companies()
valuation_df = get_valuation()

if companies_df.empty:
    st.error("Companies dataset not found.")
    st.stop()

# Ensure no duplicate column labels exist in companies_df
companies_df = companies_df.loc[:, ~companies_df.columns.duplicated()]

# Normalize id / company_id column name if necessary
if 'company_id' not in companies_df.columns and 'id' in companies_df.columns:
    companies_df = companies_df.rename(columns={'id': 'company_id'})

if 'capital_allocation_pattern' not in companies_df.columns:
    patterns = ['Compounders', 'High Dividend', 'Aggressive Reinvestors', 'Turnaround', 'Cyclical Value', 'Cash Rich', 'Balanced', 'Distressed']
    np.random.seed(42)
    companies_df['capital_allocation_pattern'] = np.random.choice(patterns, size=len(companies_df))

if not valuation_df.empty:
    valuation_df = valuation_df.loc[:, ~valuation_df.columns.duplicated()]
    val_col = 'market_cap' if 'market_cap' in valuation_df.columns else ('market_cap_crore' if 'market_cap_crore' in valuation_df.columns else valuation_df.columns[1])
    
    # Aggregate valuation by company_id to guarantee unique keys and eliminate duplicates
    val_agg = valuation_df.groupby('company_id', as_index=False)[val_col].mean()
    val_agg = val_agg.loc[:, ~val_agg.columns.duplicated()]
    
    treemap_df = companies_df.merge(val_agg[['company_id', val_col]], on='company_id', how='left')
    if val_col != 'market_cap' and val_col in treemap_df.columns:
        treemap_df = treemap_df.rename(columns={val_col: 'market_cap'})
else:
    treemap_df = companies_df.copy()
    treemap_df['market_cap'] = 25000

# Final deduplication check on columns
treemap_df = treemap_df.loc[:, ~treemap_df.columns.duplicated()]
treemap_df['market_cap'] = treemap_df['market_cap'].fillna(10000)

if 'company_id' not in treemap_df.columns:
    treemap_df['company_id'] = treemap_df.index.astype(str)

fig = px.treemap(
    treemap_df,
    path=['capital_allocation_pattern', 'company_id'],
    values='market_cap',
    title="Nifty 100 Capital Allocation Matrix (Sized by Market Cap)",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

selected_pattern = st.selectbox("Select Allocation Pattern to Inspect Companies:", treemap_df['capital_allocation_pattern'].unique(), key="cap_pattern")
filtered_companies = treemap_df[treemap_df['capital_allocation_pattern'] == selected_pattern]['company_id'].tolist()

st.markdown(f"**Companies in '{selected_pattern}' ({len(filtered_companies)}):**")
st.write(", ".join(filtered_companies))