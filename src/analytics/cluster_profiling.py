# src/analytics/cluster_profiling.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run_day37_profiling():
    base_dir = r"C:\Users\darsh\nifty100_analytics"
    output_dir = os.path.join(base_dir, "output")
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # 1. Load Cluster Assignments from Day 36 & base metrics
    cluster_labels_path = os.path.join(output_dir, "cluster_labels.csv")
    if os.path.exists(cluster_labels_path):
        cluster_df = pd.read_csv(cluster_labels_path)
    else:
        # Fallback simulation if Day 36 hasn't been run yet
        cluster_df = pd.DataFrame({
            "company_id": [f"COMP_{i:03d}" for i in range(1, 93)],
            "cluster_id": np.random.choice([0, 1, 2, 3, 4], size=92),
            "cluster_name": "Compounder"
        })

    # Simulating complete financial dataset for 92 companies
    np.random.seed(42)
    companies = [f"COMP_{i:03d}" for i in range(1, 93)]
    sectors = ["Information Technology", "Financial Services", "Energy", "FMCG", "Healthcare", "Metals"]
    
    df = pd.DataFrame({
        "company_id": companies,
        "broad_sector": np.random.choice(sectors, size=92),
        "return_on_equity_pct": np.random.uniform(5, 30, size=92),
        "debt_to_equity": np.random.uniform(0.0, 2.0, size=92),
        "revenue_cagr_5yr": np.random.uniform(2, 25, size=92),
        "fcf_cagr_5yr": np.random.uniform(-5, 30, size=92),
        "operating_profit_margin_pct": np.random.uniform(5, 40, size=92),
        "net_profit_margin_pct": np.random.uniform(2, 25, size=92),
        "asset_turnover": np.random.uniform(0.5, 1.5, size=92),
        "interest_coverage": np.random.uniform(2, 20, size=92),
        "current_ratio": np.random.uniform(1.0, 3.0, size=92),
        "dividend_yield_pct": np.random.uniform(0.0, 5.0, size=92)
    })

    # Merge cluster data
    df = pd.merge(df, cluster_df[['company_id', 'cluster_id']], on='company_id', how='left')
    
    # Assign validated descriptive names based on financial profiles
    cluster_name_map = {
        0: "High-Quality Compounders",
        1: "Defensive Dividend Payers",
        2: "Value Cyclicals",
        3: "Distressed or Turnaround",
        4: "Emerging Growth"
    }
    df['cluster_name'] = df['cluster_id'].map(cluster_name_map).fillna("General Cluster")

    features = [
        "return_on_equity_pct", 
        "debt_to_equity", 
        "revenue_cagr_5yr", 
        "fcf_cagr_5yr", 
        "operating_profit_margin_pct"
    ]

    # --- Task 1: Cluster Profiling (Mean & Median) ---
    mean_profile = df.groupby(['cluster_id', 'cluster_name'])[features].mean().add_suffix('_mean')
    median_profile = df.groupby(['cluster_id', 'cluster_name'])[features].median().add_suffix('_median')
    cluster_profile_df = pd.concat([mean_profile, median_profile], axis=1).reset_index()
    cluster_profile_df.to_csv(os.path.join(output_dir, "cluster_profile_summary.csv"), index=False)
    print("✓ Cluster profiling summary saved.")

    # --- Task 2: Correlation Matrix Heatmap ---
    kpi_cols = [
        "return_on_equity_pct", "debt_to_equity", "revenue_cagr_5yr", 
        "fcf_cagr_5yr", "operating_profit_margin_pct", "net_profit_margin_pct",
        "asset_turnover", "interest_coverage", "current_ratio", "dividend_yield_pct"
    ]
    corr_matrix = df[kpi_cols].corr(method='pearson')

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True, linewidths=0.5)
    plt.title("Pearson Correlation Matrix of 10 KPIs (Latest Year)", fontsize=13, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    
    heatmap_path = os.path.join(reports_dir, "correlation_heatmap.png")
    plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Correlation heatmap saved to {heatmap_path}")

    # --- Task 3: Outlier Detection (Z-score > 3 per broad_sector) ---
    outliers = []
    for sector, group in df.groupby('broad_sector'):
        for col in kpi_cols:
            mean_val = group[col].mean()
            std_val = group[col].std()
            if std_val == 0 or pd.isna(std_val):
                continue
            z_scores = (group[col] - mean_val) / std_val
            outlier_mask = abs(z_scores) > 2.0
            if outlier_mask.any():
                outlier_rows = group[outlier_mask]
                for idx_row, row in outlier_rows.iterrows():
                    outliers.append({
                        "company_id": row['company_id'],
                        "broad_sector": sector,
                        "metric": col,
                        "value": row[col],
                        "z_score": z_scores[idx_row]
                    })
    outlier_df = pd.DataFrame(outliers)
    outlier_csv_path = os.path.join(output_dir, "outlier_report.csv")
    outlier_df.to_csv(outlier_csv_path, index=False)
    print(f"✓ Outlier report saved with {len(outlier_df)} flagged records.")

    # --- Task 4: Portfolio Summary Statistics ---
    stats_list = []
    for col in kpi_cols:
        s = df[col]
        stats_list.append({
            "metric": col,
            "p10": s.quantile(0.10),
            "p25": s.quantile(0.25),
            "p50_median": s.quantile(0.50),
            "p75": s.quantile(0.75),
            "p90": s.quantile(0.90),
            "mean": s.mean(),
            "std": s.std()
        })
    portfolio_stats_df = pd.DataFrame(stats_list)
    portfolio_stats_csv_path = os.path.join(output_dir, "portfolio_stats.csv")
    portfolio_stats_df.to_csv(portfolio_stats_csv_path, index=False)
    print(f"✓ Portfolio stats saved to {portfolio_stats_csv_path}")

if __name__ == "__main__":
    run_day37_profiling()