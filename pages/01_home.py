import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from utils.db import get_companies, get_ratios, get_valuation, get_sectors, get_pl

# NOTE: st.set_page_config REMOVED here to prevent duplicate configuration error

st.title("🏡 Home & Executive Market Overview")
st.caption("Key summary performance indicators and sector breakdown across Nifty 100 universe")

# Load Data
companies_df = get_companies()
ratios_df = get_ratios()
mcap_df = get_valuation()
sectors_df = get_sectors()
pl_df = get_pl()

if companies_df.empty:
    st.error("Data source unavailable. Please check backend file paths.")
else:
    total_companies = len(companies_df)

    if not ratios_df.empty:
        ratios_df['clean_year'] = ratios_df['year'].astype(str).str.extract(r'(\d{4})')[0].astype(float)
        latest_ratios = ratios_df.sort_values('clean_year').groupby('company_id').last().reset_index()
    else:
        latest_ratios = pd.DataFrame()

    if not mcap_df.empty:
        mcap_df['clean_year'] = mcap_df['year'].astype(str).str.extract(r'(\d{4})')[0].astype(float)
        latest_mcap = mcap_df.sort_values('clean_year').groupby('company_id').last().reset_index()
    else:
        latest_mcap = pd.DataFrame()

    cagrs = []
    if not pl_df.empty:
        pl_df['clean_year'] = pl_df['year'].astype(str).str.extract(r'(\d{4})')[0].astype(float)
        for cid, group in pl_df.groupby('company_id'):
            group = group.sort_values('clean_year')
            s = pd.to_numeric(group['sales'], errors='coerce').dropna()
            if len(s) >= 2:
                start_val, end_val = s.iloc[0], s.iloc[-1]
                n = len(s) - 1
                if start_val > 0 and end_val > 0:
                    cagr = ((end_val / start_val) ** (1 / n) - 1) * 100
                    cagrs.append(cagr)

    avg_roe = latest_ratios['return_on_equity_pct'].dropna().mean() if not latest_ratios.empty else 0.0
    median_pe = latest_mcap['pe_ratio'].dropna().median() if not latest_mcap.empty else 0.0
    median_de = latest_ratios['debt_to_equity'].dropna().median() if not latest_ratios.empty else 0.0
    median_cagr = np.median(cagrs) if cagrs else 0.0
    debt_free_count = (latest_ratios['debt_to_equity'] == 0).sum() if not latest_ratios.empty else 0

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Companies", f"{total_companies}")
    col2.metric("Average ROE", f"{avg_roe:.2f}%")
    col3.metric("Median P/E", f"{median_pe:.2f}x")
    col4.metric("Median D/E", f"{median_de:.2f}")
    col5.metric("Median Rev CAGR (5yr)", f"{median_cagr:.2f}%")
    col6.metric("Debt-Free Companies", f"{debt_free_count}")

    st.markdown("---")

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("🧩 Sector Distribution")
        if not sectors_df.empty and 'broad_sector' in sectors_df.columns:
            sector_counts = sectors_df['broad_sector'].value_counts().reset_index()
            sector_counts.columns = ['Broad Sector', 'Count']
            
            fig = px.pie(
                sector_counts, 
                names='Broad Sector', 
                values='Count',
                hole=0.4, 
                title="Companies per Sector"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sector mapping data unavailable.")

    with right_col:
        st.subheader("🏆 Top-5 Companies by ROE Profile")
        if not latest_ratios.empty:
            top_5 = latest_ratios.sort_values('return_on_equity_pct', ascending=False).head(5)
            st.dataframe(
                top_5[['company_id', 'return_on_equity_pct', 'debt_to_equity', 'net_profit_margin_pct']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Insufficient data to compute composite quality scores.")