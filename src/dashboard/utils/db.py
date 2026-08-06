# src/dashboard/utils/db.py

import os
import numpy as np
import pandas as pd
import streamlit as st

def _get_base_dir() -> str:
    possible_paths = [
        r"C:\Users\darsh\nifty100_analytics\data\raw",
        os.path.abspath("data/raw"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "raw")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")),
        os.getcwd()
    ]
    for p in possible_paths:
        if os.path.exists(os.path.join(p, "companies.xlsx")) or os.path.exists(os.path.join(p, "peer_groups.xlsx")):
            return p
    return os.getcwd()

BASE_DIR = _get_base_dir()

def _load_excel(file_name: str) -> pd.DataFrame:
    search_dirs = [
        BASE_DIR,
        r"C:\Users\darsh\nifty100_analytics\data\raw",
        r"C:\Users\darsh\nifty100_analytics",
        os.path.abspath("data/raw"),
        os.getcwd(),
        os.path.abspath(".."),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    ]
    
    path = None
    for d in search_dirs:
        if not d: continue
        full_path = os.path.join(d, file_name)
        if os.path.exists(full_path):
            path = full_path
            break
            
    if not path or not os.path.exists(path):
        return pd.DataFrame()
        
    try:
        df_test = pd.read_excel(path, nrows=1)
        first_col = str(df_test.columns[0])
        if 'Mkt' in first_col or 'Bluestock' in first_col or '—' in first_col:
            df = pd.read_excel(path, header=1)
        else:
            df = pd.read_excel(path, header=0)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=600)
def get_companies() -> pd.DataFrame:
    df = _load_excel("companies.xlsx")
    if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
        df = df.rename(columns={'id': 'company_id'})
    return df

@st.cache_data(ttl=600)
def get_ratios(ticker: str = None) -> pd.DataFrame:
    df = _load_excel("financial_ratios.xlsx")
    if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
        df = df.rename(columns={'id': 'company_id'})
    if not df.empty and ticker and 'company_id' in df.columns:
        df = df[df['company_id'].astype(str).str.upper() == str(ticker).upper()]
    return df

@st.cache_data(ttl=600)
def get_peer_groups() -> pd.DataFrame:
    df = _load_excel("peer_groups.xlsx")
    if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
        df = df.rename(columns={'id': 'company_id'})
    return df

@st.cache_data(ttl=600)
def get_pl(ticker: str = None) -> pd.DataFrame:
    df = _load_excel("profitandloss.xlsx")
    if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
        df = df.rename(columns={'id': 'company_id'})
    if not df.empty and ticker and 'company_id' in df.columns:
        df = df[df['company_id'].astype(str).str.upper() == str(ticker).upper()]
    return df

@st.cache_data(ttl=600)
def get_bs(ticker: str = None) -> pd.DataFrame:
    df = _load_excel("balancesheet.xlsx")
    if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
        df = df.rename(columns={'id': 'company_id'})
    if not df.empty and ticker and 'company_id' in df.columns:
        df = df[df['company_id'].astype(str).str.upper() == str(ticker).upper()]
    return df

@st.cache_data(ttl=600)
def get_cf(ticker: str = None) -> pd.DataFrame:
    df = _load_excel("cashflow.xlsx")
    if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
        df = df.rename(columns={'id': 'company_id'})
    if not df.empty and ticker and 'company_id' in df.columns:
        df = df[df['company_id'].astype(str).str.upper() == str(ticker).upper()]
    return df

@st.cache_data(ttl=600)
def get_sectors() -> pd.DataFrame:
    df = _load_excel("sectors.xlsx")
    if df.empty:
        df = _load_excel("sector.xlsx")
    if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
        df = df.rename(columns={'id': 'company_id'})
    return df

@st.cache_data(ttl=600)
def get_valuation(ticker: str = None) -> pd.DataFrame:
    df = _load_excel("market_cap.xlsx")
    if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
        df = df.rename(columns={'id': 'company_id'})
    if not df.empty and ticker and 'company_id' in df.columns:
        df = df[df['company_id'].astype(str).str.upper() == str(ticker).upper()]
    return df

def find_ticker(user_input: str, companies_df: pd.DataFrame) -> str:
    if not user_input or companies_df.empty:
        return None
    clean_input = str(user_input).strip().upper().replace('.NS', '')
    if 'company_id' in companies_df.columns:
        match = companies_df[companies_df['company_id'].astype(str).str.upper() == clean_input]
        if not match.empty:
            return match.iloc[0]['company_id']
    if 'company_name' in companies_df.columns:
        match = companies_df[companies_df['company_name'].astype(str).str.upper().str.contains(clean_input, na=False)]
        if not match.empty:
            return match.iloc[0]['company_id']
    return None

def safe_display(val, default="N/A", fmt="{:.2f}"):
    """Safely format numerical values or return N/A if missing/NaN to prevent crashes."""
    if pd.isna(val) or val is None or val == np.nan:
        return default
    try:
        if isinstance(val, (int, float)):
            return fmt.format(val)
        return str(val)
    except Exception:
        return str(val)
print("Database utility module loaded successfully.")