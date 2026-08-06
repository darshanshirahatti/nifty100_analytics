# pages/05_trends.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "dashboard")))
from utils.db import get_companies, get_ratios, get_pl, find_ticker

st.markdown("## 📈 10-Year Historical Trend Analysis")
st.markdown("Analyze multi-metric historical financial performance with YoY change indicators.")

companies_df = get_companies()
if companies_df.empty:
    st.error("companies.xlsx dataset not found.")
    st.stop()

col1, col2 = st.columns([2, 2])
with col1:
    search_input = st.text_input("Search Company (Ticker or Name):", value="HDFCBANK", key="trend_search")
    ticker = find_ticker(search_input, companies_df)

if not ticker:
    st.warning("Company not found. Please check your search input.")
    st.stop()

ratios_df = get_ratios(ticker)
pl_df = get_pl(ticker)

df_combined = ratios_df if not ratios_df.empty else pl_df
if df_combined.empty:
    st.warning(f"No financial records found for {ticker}.")
    st.stop()

if 'year' in df_combined.columns:
    df_combined = df_combined.sort_values('year')

available_metrics = [c for c in df_combined.columns if c not in ['company_id', 'id', 'year', 'sector', 'sub_sector']]
if not available_metrics:
    available_metrics = df_combined.columns.tolist()

with col2:
    selected_metrics = st.multiselect("Select Metrics to Overlay (Max 3):", available_metrics, default=available_metrics[:min(2, len(available_metrics))], key="trend_metrics")

if len(selected_metrics) > 3:
    st.error("Please select a maximum of 3 metrics for clear overlay visualization.")
    st.stop()

if not selected_metrics:
    st.info("Please select at least one metric to plot.")
    st.stop()

fig = go.Figure()
years = df_combined['year'].tolist() if 'year' in df_combined.columns else list(range(len(df_combined)))

for metric in selected_metrics:
    values = df_combined[metric].tolist()
    fig.add_trace(go.Scatter(
        x=years,
        y=values,
        mode='lines+markers+text',
        name=metric,
        text=[f"{v:,.1f}" if isinstance(v, (int, float)) else str(v) for v in values],
        textposition="top center"
    ))

fig.update_layout(
    title=f"10-Year Trend for {ticker}",
    xaxis_title="Year",
    yaxis_title="Metric Value",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)