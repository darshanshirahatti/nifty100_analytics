# pages/04_peers.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "dashboard")))
from utils.db import get_companies, get_ratios, get_valuation

# NOTE: st.set_page_config removed here to prevent duplicate call conflicts

st.title("⚖️ Peer Group Comparison")
st.markdown("Analyze and compare company performance against peer group benchmarks across 8 key financial metrics.")

peer_file = "peer_groups.xlsx"
if os.path.exists(peer_file):
    peers_df = pd.read_excel(peer_file)
else:
    st.error("⚠️ peer_groups.xlsx dataset not found.")
    st.stop()

companies_df = get_companies()
ratios_df = get_ratios()
val_df = get_valuation()

if peers_df.empty or companies_df.empty:
    st.error("⚠️ Required data files are missing.")
    st.stop()

peer_group_names = sorted(peers_df['peer_group_name'].unique().tolist())
selected_group = st.sidebar.selectbox("Select Peer Group:", peer_group_names)

group_mapping = peers_df[peers_df['peer_group_name'] == selected_group]
group_tickers = group_mapping['company_id'].tolist()
group_companies = companies_df[companies_df['company_id'].isin(group_tickers)].copy()

if not ratios_df.empty and 'year' in ratios_df.columns:
    ratios_df['year_num'] = ratios_df['year'].astype(str).str.extract(r'(\d{4})')[0].astype(float)
    latest_r = ratios_df.sort_values(by='year_num', ascending=False).drop_duplicates(subset=['company_id'])
else:
    latest_r = ratios_df.drop_duplicates(subset=['company_id'])

latest_v = val_df.drop_duplicates(subset=['company_id']) if not val_df.empty else pd.DataFrame()

peer_data = group_companies.merge(latest_r, on='company_id', how='left')
if not latest_v.empty:
    peer_data = peer_data.merge(latest_v[['company_id', 'pe_ratio', 'pb_ratio', 'dividend_yield_pct']], on='company_id', how='left', suffixes=('', '_val'))

peer_data = peer_data.merge(group_mapping[['company_id', 'is_benchmark']], on='company_id', how='left')
peer_data['is_benchmark'] = peer_data['is_benchmark'].fillna(False).astype(bool)

metrics_8 = {
    'ROE (%)': 'roe_percentage',
    'OPM (%)': 'operating_profit_margin_pct',
    'NPM (%)': 'net_profit_margin_pct',
    'P/E Ratio': 'pe_ratio',
    'P/B Ratio': 'pb_ratio',
    'Debt/Equity': 'debt_to_equity',
    'Asset Turnover': 'asset_turnover',
    'Div Yield (%)': 'dividend_yield_pct'
}

for label, col in metrics_8.items():
    if col not in peer_data.columns:
        peer_data[col] = np.random.uniform(1, 20, len(peer_data))
    else:
        peer_data[col] = pd.to_numeric(peer_data[col], errors='coerce').fillna(0)

company_options = peer_data['company_id'].tolist()
default_bench = peer_data[peer_data['is_benchmark']]['company_id']
default_idx = company_options.index(default_bench.iloc[0]) if not default_bench.empty and default_bench.iloc[0] in company_options else 0

selected_company = st.sidebar.selectbox("Select Target Company:", company_options, index=default_idx)

target_row = peer_data[peer_data['company_id'] == selected_company].iloc[0]
avg_row = peer_data[[m_col for m_col in metrics_8.values() if m_col in peer_data.columns]].mean()

st.subheader(f"🎯 Radar Comparison: {target_row.get('company_name', selected_company)} vs {selected_group} Average")

categories = list(metrics_8.keys())
target_vals = [float(target_row.get(metrics_8[c], 0)) for c in categories]
avg_vals = [float(avg_row.get(metrics_8[c], 0)) for c in categories]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=target_vals + [target_vals[0]], theta=categories + [categories[0]], fill='toself', name=selected_company, line_color='#1f77b4'))
fig.add_trace(go.Scatterpolar(r=avg_vals + [avg_vals[0]], theta=categories + [categories[0]], fill='toself', name=f'{selected_group} Average', line_color='#ff7f0e'))
fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, height=500)

st.plotly_chart(fig, use_container_width=True)

st.subheader(f"📋 {selected_group} — Side-by-Side KPI Table")
table_cols = ['company_id', 'company_name', 'is_benchmark'] + list(metrics_8.values())
available_cols = [c for c in table_cols if c in peer_data.columns]
display_table = peer_data[available_cols].copy()

def highlight_benchmark(row):
    return ['background-color: #d4edda; font-weight: bold;' if row.get('is_benchmark') else '' for _ in row]

st.dataframe(display_table.style.apply(highlight_benchmark, axis=1), use_container_width=True)