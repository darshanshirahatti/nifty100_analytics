# src/dashboard/app.py

import os
import sys
import streamlit as st

# Set Streamlit Page Configuration FIRST
st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base Path Resolution
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # .../src/dashboard
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..")) # .../src
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..")) # .../nifty100_analytics
PAGES_DIR = os.path.join(PROJECT_ROOT, "pages") # Project root pages directory

# Ensure import resolution
for path in [PROJECT_ROOT, SRC_DIR, CURRENT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Custom Styling
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; font-family: 'Inter', sans-serif; }
    .main-header { 
        background: #FFFFFF; 
        border: 1px solid #E2E8F0; 
        border-radius: 12px; 
        padding: 18px 24px; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); 
    }
    .main-title { color: #1E40AF !important; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .main-subtitle { color: #64748B !important; font-size: 0.85rem; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

# Main Header Display
st.markdown("""
<div class="main-header">
    <div class="main-title">⚡ Nifty 100 Analytics</div>
    <div class="main-subtitle">Institutional Equity Research & Financial Screening Suite</div>
</div>
""", unsafe_allow_html=True)

# Navigation Mapping
page_options = {
    "🏠 01 Home & Market Overview": "01_home.py",
    "🏢 02 Company Deep-Dive Profile": "02_profile.py",
    "🔍 03 Multi-Factor Screener": "03_screener.py",
    "⚖️ 04 Peer Group Benchmarking": "04_peers.py",
    "📈 05 Historical Trend Analysis": "05_trends.py",
    "🧩 06 Sector & Sub-sector Heatmap": "06_sectors.py",
    "💳 07 Capital Allocation Patterns": "07_capital.py",
    "📊 08 Valuation Summary & Flags": "08_reports.py",
}

st.sidebar.title("Navigation")
selected_label = st.sidebar.radio("Select Module:", list(page_options.keys()))

page_file = page_options[selected_label]
target_path = os.path.join(PAGES_DIR, page_file)

# Dynamic Module Execution Context
exec_globals = {
    "__file__": target_path,
    "__name__": "__main__",
    "st": st,
    "sys": sys,
    "os": os
}

if os.path.exists(target_path):
    with open(target_path, encoding="utf-8") as f:
        code = compile(f.read(), target_path, 'exec')
        exec(code, exec_globals)
else:
    st.error(f"Page file not found at: `{target_path}`")