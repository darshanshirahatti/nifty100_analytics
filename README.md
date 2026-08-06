# ⚡ Nifty 100 Analytics

**Institutional Equity Research & Financial Screening Suite**

A comprehensive equity research and financial analytics platform for the **Nifty 100** Indian stock universe. It combines a full **ETL pipeline**, a **fundamental analytics engine**, a **config-driven stock screener**, and a modern **Streamlit dashboard** to deliver institutional-grade insights — from deep company dives to peer benchmarking, valuation flags, and capital allocation patterns.

---

## ✨ Features

- **🏠 Home & Executive Market Overview** — Aggregate KPIs (Median P/E, ROE, D/E, Revenue CAGR), sector distribution pie chart, and top companies by ROE.
- **🏢 Company Deep-Dive Profile** — Search any ticker/name for company fundamentals, ROCE/ROE, business description, and profitability trends over time.
- **🔍 Multi-Factor Screener** — Screen Nifty 100 companies across 10 fundamental metrics with 6 strategy presets (Quality, Value, Growth, Dividend, Debt-Free, Turnaround) and a composite quality score.
- **⚖️ Peer Group Benchmarking** — Compare a target company against its peer group across 8 KPIs with interactive radar charts and percentile rankings.
- **📈 10-Year Historical Trend Analysis** — Overlay up to 3 financial metrics with YoY change indicators.
- **🧩 Sector & Sub-sector Intelligence** — Bubble charts (Revenue vs. ROE, sized by Market Cap) and sector median KPIs.
- **💳 Capital Allocation Patterns** — Treemap visualization of companies grouped by capital allocation strategy (Compounders, Dividend Payers, Reinvestors, etc.).
- **📊 Valuation Summary & Flags** — Annual report / BSE filing browser with automated link validity checks (404 detection) and issuance dates.
- **📄 Valuation Flags** — Flags overvalued (Caution) and undervalued (Discount) companies vs. sector median P/E.

---

## 🧰 Tech Stack

| Layer          | Technology                                          |
|----------------|-----------------------------------------------------|
| Frontend       | Python · Streamlit · Plotly                         |
| Data Storage   | SQLite (11-table relational schema)                 |
| Data Sources   | Excel files (`data/raw/*.xlsx`)                     |
| ETL            | Pandas · OpenPyXL · custom validators/normalizers   |
| Analytics      | NumPy · Pandas · Matplotlib · OpenPyXL              |
| Testing        | Pytest                                             |

---

## 📁 Project Structure

```text
nifty100_analytics/
├─ README.md
├─ .gitignore
├─ dashboard_sprint1.py
├─ Makefile
├─ requirements.txt
├─ .streamlit/
│  └─ config.toml
├─ config/
│  └─ screener_config.yaml
├─ data/
│  ├─ nifty100.db
│  └─ raw/
│     ├─ analysis.xlsx
│     ├─ balancesheet.xlsx
│     ├─ cashflow.xlsx
│     ├─ companies.xlsx
│     ├─ documents.xlsx
│     ├─ financial_ratios.xlsx
│     ├─ market_cap.xlsx
│     ├─ peer_groups.xlsx
│     ├─ profitandloss.xlsx
│     ├─ prosandcons.xlsx
│     ├─ sectors.xlsx
│     └─ stock_prices.xlsx
├─ db/
│  └─ schema.sql
├─ output/
│  ├─ capital_allocation.csv
│  ├─ peer_comparison.xlsx
│  ├─ ratio_edge_cases.log
│  ├─ screener_output.xlsx
│  ├─ valuation_flags.csv
│  └─ valuation_summary.xlsx
├─ pages/
│  ├─ 01_home.py
│  ├─ 02_profile.py
│  ├─ 03_screener.py
│  ├─ 04_peers.py
│  ├─ 05_trends.py
│  ├─ 06_sectors.py
│  ├─ 07_capital.py
│  └─ 08_reports.py
├─ reports/
│  └─ radar_charts/
│     └─ <company>_radar.png
├─ src/
│  ├─ __init__.py
│  ├─ analytics/
│  │  ├─ __init__.py
│  │  ├─ cagr.py
│  │  ├─ cashflow_kpis.py
│  │  ├─ peer.py
│  │  ├─ populate_ratios.py
│  │  ├─ ratios.py
│  │  └─ valuation.py
│  ├─ dashboard/
│  │  ├─ __init__.py
│  │  ├─ app.py
│  │  └─ utils/
│  │     ├─ __init__.py
│  │     ├─ db.py
│  │     ├─ peer_analysis.py
│  │     └─ qa_test.py
│  ├─ etl/
│  │  ├─ __init__.py
│  │  ├─ loader.py
│  │  ├─ normaliser.py
│  │  └─ validator.py
│  ├─ screener/
│  │  ├─ __init__.py
│  │  └─ engine.py
├─ tests/
│  ├─ __init__.py
│  ├─ etl/
│  │  ├─ __init__.py
│  │  ├─ test_normaliser.py
│  │  └─ test_validator.py
│  └─ kpi/
│     ├─ __init__.py
│     ├─ test_cagr.py
│     └─ test_ratios.py
└─ .env (if present)
```

---

## 🚀 Installation & Setup

1. **Clone the repository** and navigate into the project directory:

   ```bash
   cd nifty100_analytics
   ```

2. **(Recommended) Create a virtual environment:**

   ```bash
   python -m venv .venv
   ```

   - **Windows:** `.venv\Scripts\activate`
   - **macOS / Linux:** `source .venv/bin/activate`

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   ```
   pandas>=1.3.5
   openpyxl>=3.0.9
   numpy>=1.21.0
   streamlit>=1.10.0
   pytest>=7.0.0
   ```

---

## 🖥️ Running the Dashboard

Launch the Streamlit app from the project root:

```bash
streamlit run src/dashboard/app.py
```

Then open the local URL shown in the terminal (default: `http://localhost:8501`). Use the sidebar to navigate across all 8 modules.

---

## 🧪 Running the ETL Pipeline

Populate the SQLite database from the raw Excel files:

```bash
python src/etl/loader.py
```

This:
1. Initializes the database schema (`db/schema.sql`).
2. Loads 10 core tables in dependency order.
3. Runs the `DataValidator` (DQ-01 to DQ-06 rules).
4. Exports `output/load_audit.csv` and `output/validation_failures.csv`.

---

## 📊 Running the Analytics Engine

Compute fundamental ratios, CAGR, capital allocation patterns, and peer percentiles:

```bash
python src/analytics/populate_ratios.py   # enrich financial_ratios table
python src/analytics/peer.py              # peer percentiles + radar charts
python src/analytics/valuation.py         # valuation summary + flags
```

### Screener Engine

Run the config-driven screener (generates `output/screener_output.xlsx`):

```bash
python src/screener/engine.py
```

Presets are defined in `config/screener_config.yaml`:
`quality_compounder`, `value_pick`, `growth_accelerator`, `dividend_champion`, `debt_free_blue_chip`, `turnaround_watch`.

---

## ✅ Running Tests

Execute the full test suite:

```bash
pytest
```

Or run specific suites:

```bash
pytest tests/kpi/          # CAGR & ratio calculations
pytest tests/etl/          # normaliser & validator logic
```

---

## 📦 Output Artifacts

| Artifact                          | Location                     | Description                                    |
|-----------------------------------|------------------------------|------------------------------------------------|
| Valuation Summary                 | `output/valuation_summary.xlsx` | P/E, P/B, EV/EBITDA, FCF yield, flags        |
| Valuation Flags                   | `output/valuation_flags.csv`    | Caution / Discount companies                 |
| Peer Comparison                   | `output/peer_comparison.xlsx`   | Peer KPI percentile rankings                 |
| Screener Output                   | `output/screener_output.xlsx`   | Per-preset filtered & scored results         |
| Capital Allocation                | `output/capital_allocation.csv` | Trading pattern classifications              |
| Ratio Edge Cases                  | `output/ratio_edge_cases.log`   | Data anomalies logged during analysis        |
| Radar Charts                      | `reports/radar_charts/`          | Per-company peer radar PNGs                  |

---

## 🗄️ Database Schema

SQLite database (`data/nifty100.db`) with 11 tables defined in `db/schema.sql`:

`companies`, `profitandloss`, `balancesheet`, `cashflow`, `analysis`, `documents`, `prosandcons`, `sectors`, `stock_prices`, `financial_ratios`, `peer_groups`.

---

## 📝 Notes

- `src/etl/*` handles data cleaning, validation, and loading.
- `src/analytics/*` computes KPIs, ratios, CAGR, capital allocation, and peer analytics.
- `src/screener/engine.py` orchestrates the config-driven screener pipeline.
- `src/dashboard/` contains the Streamlit app and its shared utilities (`db.py`, `peer_analysis.py`, `qa_test.py`).
- Data files are loaded from `data/raw/`; the dashboard caches queries for 10 minutes via `st.cache_data`.
