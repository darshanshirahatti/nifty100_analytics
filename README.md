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

## 🙏 Acknowledgments

Built with ❤️ for institutional-grade equity research on the Nifty 100 universe.
