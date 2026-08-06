import os
import pandas as pd

def load_peer_data() -> pd.DataFrame:
    """
    Loads peer groups dataset from data/raw directory or root path.
    """
    possible_paths = [
        r"C:\Users\darsh\nifty100_analytics\data\raw\peer_groups.xlsx",
        os.path.abspath("peer_groups.xlsx"),
        os.path.abspath("data/raw/peer_groups.xlsx")
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if not file_path:
        raise FileNotFoundError("peer_groups.xlsx could not be found in the specified directory paths.")
        
    # Read Excel file using pandas
    xls = pd.ExcelFile(file_path)
    print(f"Successfully loaded file from: {file_path}")
    print(f"Available sheets: {xls.sheet_names}")
    
    df = pd.read_excel(file_path, sheet_name=0)
    return df

if __name__ == "__main__":
    df_peers = load_peer_data()
    print("\n--- First 5 Rows ---")
    print(df_peers.head())
    
    print("\n--- Unique Peer Groups ---")
    print(df_peers['peer_group_name'].unique())