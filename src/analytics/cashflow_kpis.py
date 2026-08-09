# src/analytics/cashflow_kpis.py

import os
import numpy as np
import pandas as pd

def run_cashflow_intelligence():
    print("Running Cash Flow Intelligence Module...")

    # Define absolute paths based on project structure
    base_dir = r"C:\Users\darsh\nifty100_analytics"
    raw_dir = os.path.join(base_dir, "data", "raw")
    output_dir = os.path.join(base_dir, "output")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    def load_excel_safe(file_name):
        path = os.path.join(raw_dir, file_name)
        if os.path.exists(path):
            try:
                df_test = pd.read_excel(path, nrows=1)
                if not df_test.empty and any('Mkt' in str(c) or 'Bluestock' in str(c) for c in df_test.columns):
                    return pd.read_excel(path, header=1)
                return pd.read_excel(path)
            except Exception:
                pass
        return pd.DataFrame()

    # Load core datasets
    companies_df = load_excel_safe("companies.xlsx")
    cf_df = load_excel_safe("cashflow.xlsx")
    pl_df = load_excel_safe("profitandloss.xlsx")
    bs_df = load_excel_safe("balancesheet.xlsx")

    # Standardize column naming conventions if needed
    for df in [companies_df, cf_df, pl_df, bs_df]:
        if not df.empty and 'id' in df.columns and 'company_id' not in df.columns:
            df.rename(columns={'id': 'company_id'}, inplace=True)

    # --- Feature Calculations & Logic Placeholder ---
    # 1. CFO Quality Score: CFO / PAT ratio average over 5 years
    #    Labels: High Quality (>1.0), Moderate (0.5-1.0), Accrual Risk (<0.5)
    # 2. CapEx Intensity: abs(investing_activity) / sales * 100
    #    Labels: Asset Light (<3%), Moderate (3-8%), Capital Intensive (>8%)
    # 3. Distress Signal: CFO < 0 AND CFF > 0 in latest year
    # 4. Deleveraging Flag: CFF < 0 AND borrowings declining YoY

    # Defining output structures
    columns_intelligence = [
        "company_id", "sector", "cfo_quality_score", "cfo_quality_label", 
        "capex_intensity_pct", "capex_label", "fcf_cagr_5yr", "fcf_conversion_pct", 
        "distress_flag", "deleveraging_flag", "capital_allocation_label"
    ]
    
    intelligence_df = pd.DataFrame(columns=columns_intelligence)
    
    # Save cashflow intelligence workbook
    output_excel_path = os.path.join(output_dir, "cashflow_intelligence.xlsx")
    intelligence_df.to_excel(output_excel_path, index=False)
    print(f"Successfully generated: {output_excel_path}")

    # Defining distress alerts structure
    columns_distress = ["company_id", "sector", "cfo_value", "cff_value", "latest_net_profit"]
    distress_df = pd.DataFrame(columns=columns_distress)
    
    # Save distress alerts CSV
    output_csv_path = os.path.join(output_dir, "distress_alerts.csv")
    distress_df.to_csv(output_csv_path, index=False)
    print(f"Successfully generated: {output_csv_path}")

if __name__ == "__main__":
    run_cashflow_intelligence()

print("Cash Flow Intelligence Analysis Complete. check output files in the output directory ")