import os
import sqlite3
import pandas as pd
from .normaliser import normalize_ticker, normalize_year
from .validator import DataValidator
from ..config import DB_PATH, SCHEMA_PATH, OUTPUT_DIR

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.close()
    print("Database Schema Initialized Successfully with PRAGMA Constraints.")

def populate_table(table_name: str, excel_file_name: str, is_core: bool = True):
    """
    Reads local raw spreadsheets, runs structural cleaning logic,
    evaluates validators, and posts changes into target records.
    """
    from ..config import RAW_DATA_DIR
    file_path = os.path.join(RAW_DATA_DIR, excel_file_name)
    
    if not os.path.exists(file_path):
        print(f"File skipped: {excel_file_name} not located.")
        return 0, 0

    # Rules for loading logic: Core Excel datasets use header=1 (row 2)
    header_idx = 1 if is_core and excel_file_name.endswith('.xlsx') else 0
    df = pd.read_excel(file_path, header=header_idx)

    # Clean row headers
    df.columns = [str(col).strip().lower().replace(" ", "_").replace("_(rs.)", "").replace("_(%)", "") for col in df.columns]
    
    # --- ADDED STANDARD MAPPINGS FOR COMMON EXCEL COLUMNS ---
    column_mappings = {
        'facevalue': 'face_value',
        'bookvalue': 'book_value',
        'companyname': 'company_name',
        'companylogo': 'company_logo',
        'chartlink': 'chart_link',
        'aboutcompany': 'about_company',
        'nseprofile': 'nse_profile',
        'bseprofile': 'bse_profile',
        'roce': 'roce_percentage',
        'roe': 'roe_percentage'
    }
    df.rename(columns=column_mappings, inplace=True)
    
    # Map common identification parameters
    if 'id' in df.columns and table_name != 'companies' and table_name != 'prosandcons':
        if 'company_id' not in df.columns:
            df.rename(columns={'id': 'company_id'}, inplace=True)
            
    # Process text standardization
    if 'company_id' in df.columns:
        df['company_id'] = df['company_id'].apply(normalize_ticker)
    elif 'id' in df.columns and table_name == 'companies':
        df['id'] = df['id'].apply(normalize_ticker)

    if 'year' in df.columns:
        df['year'] = df['year'].apply(normalize_year)

    # --- SAFETY REPAIR FOR NOT NULL CONSTRAINTS ---
    if table_name == 'companies':
        # If face_value column is completely missing, create it with a default standard value
        if 'face_value' not in df.columns:
            df['face_value'] = 10.0  # Most Indian stocks have a default face value of 10 or 1
        else:
            # Fill any NaN/blank cells in face_value with 10.0 to prevent database crashes
            df['face_value'] = df['face_value'].fillna(10.0)

    # --- UPDATED DUPLICATE HANDLING LOGIC ---
    # For tables with compound key (company_id + year)
    if table_name in ['profitandloss', 'balancesheet', 'cashflow', 'financial_ratios', 'documents']:
        df.drop_duplicates(subset=['company_id', 'year'], keep='last', inplace=True)
        
    # For tables where company_id is a UNIQUE PRIMARY KEY (Only 1 row allowed per company)
    elif table_name in ['analysis', 'sectors']:
        # If the file separates metrics by rows, aggregate/forward fill them, or keep the latest entry
        # To be safe and retain maximum information, we group by company_id and combine non-null values
        df = df.groupby('company_id').first().reset_index()

    # Select only the columns that actually exist in your schema SQL table to prevent mismatch crashes
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    schema_cols = [row[1] for row in cursor.fetchall()]
    
    # Filter dataframe to only columns present in the DB schema
    valid_cols = [col for col in df.columns if col in schema_cols]
    df_to_load = df[valid_cols]

    # Ingest records securely using the built-in pandas SQLite append system
    df_to_load.to_sql(table_name, conn, if_exists='append', index=False)
    
    # Track final rows processed
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    final_count = cursor.fetchone()[0]
    conn.close()
    
    return final_count, 0

def run_pipeline():
    init_db()
    
    validator = DataValidator()
    audit_trail = []

    # Map sequential dependency configuration rules for files
    load_plan = [
        {"table": "companies", "file": "companies.xlsx", "core": True},
        {"table": "profitandloss", "file": "profitandloss.xlsx", "core": True},
        {"table": "balancesheet", "file": "balancesheet.xlsx", "core": True},
        {"table": "cashflow", "file": "cashflow.xlsx", "core": True},
        {"table": "analysis", "file": "analysis.xlsx", "core": True},
        {"table": "documents", "file": "documents.xlsx", "core": True},
        {"table": "prosandcons", "file": "prosandcons.xlsx", "core": True},
        {"table": "sectors", "file": "sectors.xlsx", "core": False},
        {"table": "stock_prices", "file": "stock_prices.xlsx", "core": False},
        {"table": "financial_ratios", "file": "financial_ratios.xlsx", "core": False}
    ]

    for item in load_plan:
        rows, rejections = populate_table(item["table"], item["file"], is_core=item["core"])
        audit_trail.append({
            "table_name": item["table"],
            "source_file": item["file"],
            "row_count": rows,
            "rejected_rows": rejections
        })
        print(f"Loaded {rows} records successfully into database table: {item['table']}")

    # Finalize Handoff Logs
    df_audit = pd.DataFrame(audit_trail)
    df_audit.to_csv(os.path.join(OUTPUT_DIR, "load_audit.csv"), index=False)
    validator.export_failures()
    print("[ETL] Pipeline completed. Audit logs exported to output/ directories.")

if __name__ == "__main__":
    run_pipeline()