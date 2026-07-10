import pandas as pd
import numpy as np

class DataValidator:
    def __init__(self):
        self.failures = [] # Logs dictionary registers for validation_failures.csv

    def log_failure(self, rule_id: str, rule_name: str, company_id: str, year: str, severity: str, details: str):
        self.failures.append({
            "rule_id": rule_id,
            "rule_name": rule_name,
            "company_id": company_id,
            "year": year,
            "severity": severity,
            "details": details
        })

    def validate_companies(self, df_companies: pd.DataFrame):
        # DQ-01: Company PK Uniqueness
        if df_companies['id'].duplicated().any():
            dupes = df_companies['id'][df_companies['id'].duplicated()].tolist()
            for d in dupes:
                self.log_failure("DQ-01", "Company PK Uniqueness", d, "N/A", "CRITICAL", "Duplicate Master Company Key Found.")

    def validate_financial_statements(self, df: pd.DataFrame, table_name: str, is_bank_table: bool = False):
        """ Runs transactional check patterns for statements (P&L, BS, CF) """
        # DQ-02: Composite Primary Key Check
        dupe_mask = df.duplicated(subset=['company_id', 'year'], keep=False)
        if dupe_mask.any():
            for idx, row in df[dupe_mask].iterrows():
                self.log_failure("DQ-02", f"{table_name} PK Uniqueness", row['company_id'], row['year'], "CRITICAL", f"Duplicate row in {table_name}")

        # Core mathematical relationship evaluations
        for idx, row in df.iterrows():
            comp = row['company_id']
            yr = row['year']

            # DQ-04: Balance Sheet Identity Equation
            if table_name == "balancesheet":
                ta = float(row.get('total_assets', 0))
                tl = float(row.get('total_liabilities', 0))
                if ta > 0 and (abs(ta - tl) / ta) >= 0.01:
                    self.log_failure("DQ-04", "BS Balance Check", comp, yr, "WARNING", f"Assets ({ta}) != Liabilities ({tl}) mismatch > 1%")

            # DQ-05: Operating Margin Cross Check Validation
            if table_name == "profitandloss":
                sales = float(row.get('sales', 0))
                op = float(row.get('operating_profit', 0))
                reported_opm = float(row.get('opm_percentage', 0))
                if sales > 0:
                    calc_opm = (op / sales) * 100
                    if abs(reported_opm - calc_opm) > 1.0:
                        self.log_failure("DQ-05", "OPM Cross-Check", comp, yr, "WARNING", f"Reported OPM {reported_opm}% differs from computed {calc_opm:.2%}%")
                
                # DQ-06: Non-Zero/Positive Income confirmation for core sectors
                if not is_bank_table and sales <= 0:
                    self.log_failure("DQ-06", "Positive Sales Check", comp, yr, "WARNING", f"Zero or negative sales found: {sales}")

    def export_failures(self, output_path: str = "output/validation_failures.csv"):
        df_out = pd.DataFrame(self.failures)
        if df_out.empty:
            df_out = pd.DataFrame(columns=["rule_id", "rule_name", "company_id", "year", "severity", "details"])
        df_out.to_csv(output_path, index=False)
        return df_out
print("DataValidator module loaded successfully.")