import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import get_companies, get_ratios, get_valuation, get_pl, find_ticker

# NOTE: st.set_page_config REMOVED here to prevent duplicate configuration error

st.title("🏢 Company Deep-Dive Profile")

companies_df = get_companies()

if companies_df.empty:
    st.error("Companies database is unavailable.")
else:
    ticker_options = companies_df['company_id'].unique().tolist()
    
    col_input, col_select = st.columns([1, 1])
    with col_input:
        user_input = st.text_input("Enter Company Ticker (e.g. ABB, ADANIENT):", value="ABB")
    with col_select:
        selected_dropdown = st.selectbox("Or Pick from List:", options=["-- Select --"] + ticker_options)

    active_input = user_input if user_input and user_input != "ABB" else (
        selected_dropdown if selected_dropdown != "-- Select --" else user_input
    )
    
    ticker = find_ticker(active_input, companies_df)

    if not ticker:
        st.error(f"⚠️ Ticker **'{active_input}'** not found — please select or enter a valid ticker.")
    else:
        company_info = companies_df[companies_df['company_id'] == ticker].iloc[0]
        ratios_df = get_ratios(ticker)
        pl_df = get_pl(ticker)
        val_df = get_valuation(ticker)

        st.success(f"Loaded Profile for: **{company_info.get('company_name', ticker)}** ({ticker})")

        c1, c2, c3 = st.columns(3)
        c1.write(f"**Face Value:** {company_info.get('face_value', 'N/A')}")
        c2.write(f"**ROCE:** {company_info.get('roce_percentage', 'N/A')}%")
        c3.write(f"**ROE:** {company_info.get('roe_percentage', 'N/A')}%")

        if pd.notna(company_info.get('about_company')):
            st.info(company_info.get('about_company'))

        st.markdown("---")
        
        if not ratios_df.empty:
            st.subheader("📈 Key Ratio Trends Over Time")
            fig = px.line(
                ratios_df, 
                x='year', 
                y=['return_on_equity_pct', 'net_profit_margin_pct', 'operating_profit_margin_pct'],
                markers=True,
                title="Profitability Metrics History"
            )
            st.plotly_chart(fig, use_container_width=True)  