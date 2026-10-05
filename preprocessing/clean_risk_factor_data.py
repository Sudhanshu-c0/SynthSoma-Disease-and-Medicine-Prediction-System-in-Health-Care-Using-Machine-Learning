import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / 'datasets' / 'raw' / 'disease_riskFactors.csv'
CLEANED_PATH = BASE_DIR / 'datasets' / 'cleaned' / 'risk_factor_cleaned.csv'

def clean_risk_factor_data():
    """
    Cleans raw disease risk factors dataset.
    """
    if not RAW_PATH.exists():
        print(f"Raw risk factors dataset not found at {RAW_PATH}")
        return None

    df_raw = pd.read_csv(RAW_PATH, encoding='latin1')
    for col in df_raw.columns:
        if df_raw[col].dtype == object:
            df_raw[col] = df_raw[col].astype(str).str.strip()

    print(f"Cleaned risk factor dataset: {df_raw.shape}")
    return df_raw

if __name__ == '__main__':
    clean_risk_factor_data()
