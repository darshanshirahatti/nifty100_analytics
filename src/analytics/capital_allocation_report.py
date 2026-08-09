# src/analytics/capital_allocation_report.py

import os
import pandas as pd
import numpy as np

def run_capital_allocation_report():
    print("Running Capital Allocation Report Module (Day 32)...")

    # Define absolute paths based on project structure
    base_dir = r"C:\Users\darsh\nifty100_analytics"
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # 1. Verify capital_allocation.csv from Sprint 2
    cap_alloc_path = os.path.join(output_dir, "capital_allocation.csv")
    if not os.path.exists(cap_alloc_path):
        print(f"Warning: {cap_alloc_path} not found. Please ensure Sprint 2 outputs are generated.")
        return

    df_cap = pd.read_csv(cap_alloc_path)
    print(f"Loaded capital_allocation.csv successfully with shape: {df_cap.shape}")

    # 2. Generate distribution summary: count of companies in each of the 8 patterns for the latest year
    if 'year' in df_cap.columns and 'pattern' in df_cap.columns:
        latest_year = df_cap['year'].max()
        df_latest = df_cap[df_cap['year'] == latest_year]
        distribution_summary = df_latest['pattern'].value_counts().reset_index()
        distribution_summary.columns = ['pattern', 'company_count']
        
        print(f"\n--- Distribution Summary for Latest Year ({latest_year}) ---")
        print(distribution_summary.to_string(index=False))
        
        # Save distribution summary
        dist_output_path = os.path.join(output_dir, "pattern_distribution_latest.csv")
        distribution_summary.to_csv(dist_output_path, index=False)

    # 3. Add capital allocation column to cashflow_intelligence.xlsx
    cf_intel_path = os.path.join(output_dir, "cashflow_intelligence.xlsx")
    if os.path.exists(cf_intel_path):
        try:
            df_intel = pd.read_excel(cf_intel_path)
            latest_patterns = df_cap.sort_values('year').groupby('company_id').tail(1)[['company_id', 'pattern']]
            
            df_intel = df_intel.merge(latest_patterns, on='company_id', how='left')
            if 'capital_allocation_label' in df_intel.columns:
                df_intel['capital_allocation_label'] = df_intel['pattern'].fillna(df_intel['capital_allocation_label'])
            else:
                df_intel['capital_allocation_label'] = df_intel['pattern']
                
            if 'pattern' in df_intel.columns:
                df_intel.drop(columns=['pattern'], inplace=True)
                
            df_intel.to_excel(cf_intel_path, index=False)
            print(f"\nUpdated {cf_intel_path} with latest capital allocation labels.")
        except Exception as e:
            print(f"Error updating cashflow_intelligence.xlsx: {e}")

    # 4. Build text/CSV report showing companies that changed their pattern year-over-year
    if {'company_id', 'year', 'pattern'}.issubset(df_cap.columns):
        df_sorted = df_cap.sort_values(by=['company_id', 'year'])
        df_sorted['previous_pattern'] = df_sorted.groupby('company_id')['pattern'].shift(1)
        
        # Filter rows where pattern changed from previous year
        changes_df = df_sorted[
            df_sorted['previous_pattern'].notna() & 
            (df_sorted['pattern'] != df_sorted['previous_pattern'])
        ].copy()
        
        pattern_changes_path = os.path.join(output_dir, "pattern_changes.csv")
        changes_df[['company_id', 'year', 'previous_pattern', 'pattern']].to_csv(pattern_changes_path, index=False)
        print(f"\nGenerated pattern changes report: {pattern_changes_path} (Total shifts detected: {len(changes_df)})")

if __name__ == "__main__":
    run_capital_allocation_report()

print("Capital allocation report generated")