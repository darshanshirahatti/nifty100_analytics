# Nifty 100 Analytics

A full-stack financial analytics and research platform for the Nifty 100 universe. The project combines ETL ingestion, a SQLite-backed analytics layer, a FastAPI backend, a Streamlit dashboard, and a set of automated quality tests to support company screening, valuation checks, peer benchmarking, and operational reporting.

---

## Overview

This repository supports:

- ETL ingestion from raw Excel files into a normalized SQLite database
- Fundamental ratio and KPI calculations
- Screener-based stock filtering and strategy presets
- Company, sector, and peer analysis views
- FastAPI endpoints for programmatic access
- Streamlit dashboards for analyst workflows
- PDF/HTML reporting and archival utilities
- Automated test coverage for API, ETL, KPI, and DQ rules

---

## Core Features

- Executive summary and market overview dashboards
- Company profile drill-downs with fundamentals and trend views
- Multi-factor screener using config-driven presets
- Peer comparison and radar-chart benchmarking
- Sector and capital allocation views
- Valuation risk and quality flag generation
- PDF analyst guide generation
- SQLite database optimization utilities
- Deliverable archival packaging for final output sets

---

## Tech Stack

- Python 3.7+
- Streamlit
- FastAPI
- SQLite
- Pandas, NumPy, OpenPyXL, Plotly, ReportLab
- Pytest

---

## Project Structure

```text
nifty100_analytics/
├─ README.md
├─ .gitignore
├─ Makefile
├─ requirements.txt
├─ conftest.py
├─ dashboard_sprint1.py
├─ config/
│  └─ screener_config.yaml
├─ data/
│  ├─ nifty100.db
│  └─ raw/
├─ db/
│  └─ schema.sql
├─ docs/
│  └─ analyst_guide.pdf
├─ output/
│  ├─ final_deliverables/
│  ├─ perf_notes.md
│  ├─ validation_failures.csv
│  └─ ...
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
│  ├─ pytest_report.html
│  └─ ...
├─ src/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ analytics/
│  ├─ api/
│  ├─ dashboard/
│  ├─ etl/
│  ├─ nlp/
│  ├─ screener/
│  └─ utils/
│     ├─ archive_deliverables.py
│     ├─ generate_acceptance_checklist.py
│     ├─ generate_guide.py
│     └─ __init__.py
├─ tests/
│  ├─ api/
│  ├─ dq/
│  ├─ etl/
│  ├─ kpi/
│  └─ performance/
└─ .venv/
```

---

## Setup

1. Clone the repository.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Windows PowerShell Quick Start

From the repository root in PowerShell:

```powershell
cd C:\Users\darsh\nifty100_analytics
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.etl.loader
uvicorn src.api.main:app --reload --port 8000
streamlit run src/dashboard/app.py
pytest tests/ --html=reports/pytest_report.html --self-contained-html -v
```

Use separate terminals for the API and dashboard if needed.

---

## Run the API

From the project root:

```bash
uvicorn src.api.main:app --reload --port 8000
```

The API exposes endpoints such as company data, screener filters, and sector/valuation views.

---

## Run the Dashboard

```bash
after activating the venv:
streamlit run src/dashboard/app.py
```

Open the local Streamlit URL displayed in the terminal.

---

## Load Data and Run ETL

```bash
python -m src.etl.loader
```

This populates the SQLite database and validates the imported records using the project rules.

---

## Generate the Analyst Guide

```bash
python -m src.utils.generate_guide
```

This writes the report to:

```text
docs/analyst_guide.pdf
```

---

## Archive Deliverables

```bash
python -m src.utils.archive_deliverables
```

This copies the final deliverables package into:

```text
output/final_deliverables/
```

---

## Run Tests

```bash
pytest tests/ --html=reports/pytest_report.html --self-contained-html -v
```

Current project status includes successful execution of the main test suite with passing core coverage, while the explicit performance checks are set to skip when the API is not running.

---

## Notes

- The project uses a centralized config file for database and path handling: `src/config.py`.
- System and generated artifacts are intentionally excluded from version control via `.gitignore`.
- Performance tests are designed to skip cleanly when the FastAPI service is not started.
- The repository is structured for local analyst workflows and lightweight production-style validation.

#### API Tests (3 tests)
- `test_companies.py` — Company list & detail retrieval endpoints with sector data
- `test_screener.py` — Screener filter validation & parameter checks
- `test_health.py` — API health check endpoint with table statistics

#### Data Quality Tests (14 tests)
- `test_rules.py` — DQ validation rules (RULE_01 through RULE_14):
  - RULE_01-02: Negative debt/revenue detection
  - RULE_03-04: ROE bounds & current ratio validation
  - RULE_05-06: Interest coverage & operating margin checks
  - RULE_07: Missing company ID detection
  - RULE_08-14: Asset turnover, dividend yield, NPM, D/E, FCF, year, promoter holding

#### ETL Tests (11 tests)
- Company, financial, and CSV file loading tests

#### KPI Tests (27 tests)
- CAGR calculations (turnaround, decline, normal cases)
- ROE, D/E, ICR, asset turnover calculations
- Edge case handling

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

## 🗄️ Database

SQLite database (`data/nifty100.db`) with centralized path configuration in `src/config.py`.

**Key Features:**
- Single source of truth for all database paths (ETL, API, Analytics, Tests)
- Ensures all modules access the same database file
- Absolute path resolution for cross-module compatibility

**11-Table Schema:**
`companies`, `profitandloss`, `balancesheet`, `cashflow`, `analysis`, `documents`, `prosandcons`, `sectors`, `stock_prices`, `financial_ratios`, `peer_groups`.

**Column Naming Convention:**
- Primary IDs: `id` (companies), `company_id` (all other tables)
- KPIs: `return_on_equity_pct`, `roce_percentage`, `debt_to_equity`, etc.
- Temporal: `year` (YYYY-MM format)
- Sector Data: `broad_sector`, `sub_sector`, `market_cap_category`

---

## � API Endpoints

A production-grade FastAPI backend is available at `src/api/main.py` with the following features:

### Middleware
- **CORS** — Enabled for all origins (internal use)
- **Request Logging** — Logs method, path, duration, and status code
- **SQLite Connection Pool** — Efficient database access

### Router Modules (`/api/v1`)
- `/companies` — Query company fundamentals, detailed profiles
- `/screener` — Execute stock screener with custom filters & validation
- `/peers` — Peer benchmarking and percentile rankings
- `/sectors` — Sector-level aggregations and statistics
- `/portfolio` — Portfolio analysis and performance metrics
- `/valuation` — Valuation flags, P/E, P/B summaries
- `/documents` — Annual reports and BSE filing browser
- `/health` — Service health check

Start the API server:
```bash
cd src/api && uvicorn main:app --reload
```

API documentation:
- **Interactive Docs:** `http://localhost:8000/docs` (Swagger UI)
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI Schema:** `src/api/docs/openapi.json`

---

## 📝 Notes

- `src/config.py` provides centralized path configuration for all modules
- `src/etl/*` handles data cleaning, validation, and loading
- `src/analytics/*` computes KPIs, ratios, CAGR, capital allocation, and peer analytics
- `src/screener/engine.py` orchestrates the config-driven screener pipeline
- `src/api/` provides FastAPI endpoints with CORS & request logging middleware
- `src/nlp/` handles pros & cons parsing and generation
- `src/dashboard/` contains the Streamlit app and shared utilities
- Data files are loaded from `data/raw/`; the dashboard caches queries for 10 minutes via `st.cache_data`
- All database connections use the centralized `DB_PATH` from `src/config.py`

---

## 📋 Requirements

- **Python 3.8+**
- **pip** or **conda**
- **SQLite3** (usually included)
- Excel files in `data/raw/` (sample structure in documentation)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and write tests
4. Run `pytest` to ensure all tests pass
5. Commit your changes: `git commit -am 'Add your feature'`
6. Push to the branch: `git push origin feature/your-feature`
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see LICENSE file for details.

---

## 💬 Support & Contact

For issues, questions, or suggestions:
- Open an [issue](../../issues) on GitHub
- Submit a [pull request](../../pulls) with improvements
- Contact the maintainers through the repository

---

## � Project Deliverables Tracker

All **23 deliverables** completed and ready for project sign-off.

| ID | Sprint | Deliverable | Location | Status |
|---|---|---|---|---|
| D-01 | Sprint 1 | nifty100.db | data/nifty100.db | ✅ Done |
| D-02 | Sprint 1 | load_audit.csv | output/load_audit.csv | ✅ Done |
| D-03 | Sprint 1 | validation_failures.csv | output/validation_failures.csv | ✅ Done |
| D-04 | Sprint 1 | exploratory_queries.sql | notebooks/exploratory_queries.sql | ✅ Done |
| D-05 | Sprint 2 | financial_ratios table | data/nifty100.db → financial_ratios | ✅ Done |
| D-06 | Sprint 2 | capital_allocation.csv | output/capital_allocation.csv | ✅ Done |
| D-07 | Sprint 3 | screener_output.xlsx | output/screener_output.xlsx | ✅ Done |
| D-08 | Sprint 3 | screener_config.yaml | config/screener_config.yaml | ✅ Done |
| D-09 | Sprint 3 | peer_comparison.xlsx | output/peer_comparison.xlsx | ✅ Done |
| D-10 | Sprint 3 | 92 Radar Charts | reports/radar_charts/ | ✅ Done |
| D-11 | Sprint 4 | Streamlit Dashboard (8 Screens) | src/dashboard/app.py | ✅ Done |
| D-12 | Sprint 4 | valuation_summary.xlsx | output/valuation_summary.xlsx | ✅ Done |
| D-13 | Sprint 5 | cashflow_intelligence.xlsx | output/cashflow_intelligence.xlsx | ✅ Done |
| D-14 | Sprint 5 | pros_cons_generated.csv | output/pros_cons_generated.csv | ✅ Done |
| D-15 | Sprint 5 | analysis_parsed.csv | output/analysis_parsed.csv | ✅ Done |
| D-16 | Sprint 5 | 92 Company Tearsheets | reports/tearsheets/ | ✅ Done |
| D-17 | Sprint 5 | 11 Sector Reports | reports/sector/ | ✅ Done |
| D-18 | Sprint 5 | Portfolio Summary PDF | reports/portfolio/ | ✅ Done |
| D-19 | Sprint 6 | cluster_labels.csv | output/cluster_labels.csv | ✅ Done |
| D-20 | Sprint 6 | FastAPI Server (16 Endpoints) | src/api/main.py | ✅ Done |
| D-21 | Sprint 6 | pytest_report.html | reports/pytest_report.html | ✅ Done |
| D-22 | Sprint 6 | analyst_guide.pdf | docs/analyst_guide.pdf | ✅ Done |
| D-23 | Sprint 6 | acceptance_checklist.pdf | docs/acceptance_checklist.pdf | ✅ Done |

---

## 🎯 Quick Reference — Key Commands

### Data & Analytics
```bash
make load       # Load all Excel files into nifty100.db (Day 05)
make ratios     # Generate and populate the financial_ratios table
make report     # Generate all company tearsheets, sector reports, and portfolio report
```

### Testing & QA
```bash
make test       # Run all pytest tests and generate reports/pytest_report.html
```

### Applications
```bash
make dashboard  # Launch Streamlit Dashboard on localhost:8501
make api        # Launch FastAPI server on localhost:8000
```

### Maintenance
```bash
make clean      # Remove cache (.pyc) and test artifacts. Database remains untouched.
```

---

## 📌 Important Rules

### Data Loading & Processing
- Use **`pd.read_excel(path, header=1)`** for all core Excel files.
- Always normalize **`company_id`** (trim spaces and convert to uppercase) before joins.
- All monetary values are stored in **INR Crore**.

### Business Logic
- Skip **Financials** sector while applying the D/E screener filter.
- If CAGR has a negative base year, return **TURNAROUND** instead of calculating CAGR.
- If Interest Expense = 0, display **Debt Free** instead of dividing by zero.

### Documentation & Testing
- Clearly label simulated datasets (stock_prices, market_cap) as **SIMULATED** in dashboards and reports.
- Run **`make test`** before every Git commit. **Zero test failures are mandatory.**

---

## �🙏 Acknowledgments

Built with ❤️ for institutional-grade equity research on the Nifty 100 universe.
