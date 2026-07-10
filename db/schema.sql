-- Enforce database schema constraints
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS peer_groups;
DROP TABLE IF EXISTS stock_prices;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS financial_ratios;
DROP TABLE IF EXISTS prosandcons;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS analysis;
DROP TABLE IF EXISTS cashflow;
DROP TABLE IF EXISTS balancesheet;
DROP TABLE IF EXISTS profitandloss;
DROP TABLE IF EXISTS companies;

-- Table 1: Companies (Master Ticker Map)
CREATE TABLE companies (
    id VARCHAR(20) PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    company_logo TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value NUMERIC NOT NULL,
    book_value NUMERIC,
    roce_percentage NUMERIC,
    roe_percentage NUMERIC
);

-- Table 2: Profit And Loss
CREATE TABLE profitandloss (
    company_id VARCHAR(20) NOT NULL,
    year VARCHAR(7) NOT NULL,
    sales NUMERIC NOT NULL,
    expenses NUMERIC,
    operating_profit NUMERIC,
    opm_percentage NUMERIC,
    other_income NUMERIC,
    interest NUMERIC,
    depreciation NUMERIC,
    profit_before_tax NUMERIC,
    tax_percentage NUMERIC,
    net_profit NUMERIC,
    eps NUMERIC,
    dividend_payout NUMERIC,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 3: Balance Sheet
CREATE TABLE balancesheet (
    company_id VARCHAR(20) NOT NULL,
    year VARCHAR(7) NOT NULL,
    equity_capital NUMERIC NOT NULL,
    reserves NUMERIC,
    borrowings NUMERIC,
    other_liabilities NUMERIC,
    total_liabilities NUMERIC NOT NULL,
    fixed_assets NUMERIC,
    cwip NUMERIC,
    investments NUMERIC,
    other_asset NUMERIC,
    total_assets NUMERIC NOT NULL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 4: Cash Flow
CREATE TABLE cashflow (
    company_id VARCHAR(20) NOT NULL,
    year VARCHAR(7) NOT NULL,
    operating_activity NUMERIC,
    investing_activity NUMERIC,
    financing_activity NUMERIC,
    net_cash_flow NUMERIC,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 5: Analysis Text Gaps
CREATE TABLE analysis (
    company_id VARCHAR(20) PRIMARY KEY,
    compounded_sales_growth TEXT,
    compounded_profit_growth TEXT,
    stock_price_cagr TEXT,
    roe TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 6: Documents Repositories
CREATE TABLE documents (
    company_id VARCHAR(20) NOT NULL,
    year INTEGER NOT NULL,
    annual_report TEXT,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 7: Pros and Cons
CREATE TABLE prosandcons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id VARCHAR(20) NOT NULL,
    pros TEXT,
    cons TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 8: Sectors Taxonomy Mapping
CREATE TABLE sectors (
    company_id VARCHAR(20) PRIMARY KEY,
    broad_sector VARCHAR(100) NOT NULL,
    sub_sector VARCHAR(100),
    index_weight_pct NUMERIC,
    market_cap_category VARCHAR(50),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 9: Stock Prices History
CREATE TABLE stock_prices (
    company_id VARCHAR(20) NOT NULL,
    date VARCHAR(10) NOT NULL,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume INTEGER,
    adjusted_close NUMERIC,
    PRIMARY KEY (company_id, date),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 10: Financial Ratios
CREATE TABLE financial_ratios (
    company_id VARCHAR(20) NOT NULL,
    year VARCHAR(7) NOT NULL,
    net_profit_margin_pct NUMERIC,
    operating_profit_margin_pct NUMERIC,
    return_on_equity_pct NUMERIC,
    debt_to_equity NUMERIC,
    interest_coverage NUMERIC,
    asset_turnover NUMERIC,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Table 11: Peer Groups (Supplementary Setup)
CREATE TABLE peer_groups (
    company_id VARCHAR(20) NOT NULL,
    peer_group_name VARCHAR(100) NOT NULL,
    is_benchmark INT DEFAULT 0,
    PRIMARY KEY (company_id, peer_group_name),
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);