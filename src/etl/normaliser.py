import re

def normalize_ticker(ticker: str) -> str:
    """
    Standardizes company identifiers to uppercase stripped NSE tickers.
    Removes whitespace, newlines, and hidden formatting characters.
    """
    if not isinstance(ticker, str):
        return str(ticker).strip().upper()
    # Strip any potential newline characters or whitespace anomalies found in source files
    return ticker.strip().replace('\n', '').replace('\r', '').upper()

def normalize_year(year_val) -> str:
    """
    Normalizes inconsistent financial year notations to standard 'YYYY-MM'.
    Handles: 'Mar-23' -> '2023-03', 'Mar-2024' -> '2024-03', '2023' -> '2023-03' (default).
    """
    if not year_val or str(year_val).strip() == "":
        return "0000-00"
    
    val_str = str(year_val).strip()
    
    # Pattern 1: Mon-YY or Mon-YYYY (e.g., Mar-23, Mar-2024)
    match_mon_year = re.match(r'^([A-Za-z]{3})[-/](\d{2,4})$', val_str)
    if match_mon_year:
        month_str, year_digits = match_mon_year.groups()
        # Map month text to 2 digit standard
        months_map = {
            'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
            'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
        }
        mm = months_map.get(month_str.upper(), "03") # Fallback to standard March close if uncertain
        
        if len(year_digits) == 2:
            # Assume 20xx for modern financial cycles
            yyyy = f"20{year_digits}"
        else:
            yyyy = year_digits
        return f"{yyyy}-{mm}"
    
    # Pattern 2: Pure YYYY digit string (e.g., 2023)
    match_pure_year = re.match(r'^(\d{4})$', val_str)
    if match_pure_year:
        return f"{match_pure_year.group(1)}-03"
        
    return val_str # Fallback return if structure matches custom regex elsewhere
print(normalize_year("Mar-23"))