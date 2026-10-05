import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / 'datasets' / 'raw' / 'disease_medicine.csv'
CLEANED_PATH = BASE_DIR / 'datasets' / 'cleaned' / 'medicine_prediction_cleaned.csv'

def clean_medicine_data():
    """
    Cleans raw disease medicine dataset, parsing Latin1 encoding and removing unused columns.
    """
    if not RAW_PATH.exists():
        print(f"Raw medicine dataset not found at {RAW_PATH}")
        return None

    df_raw = pd.read_csv(RAW_PATH, encoding='latin1')
    keep_cols = ['Medicine_ID', 'Medicine_Name', 'Disease_ID', 'Medicine_Composition', 'Medicine_Description']
    existing_cols = [c for c in keep_cols if c in df_raw.columns]
    df_clean = df_raw[existing_cols].copy()

    for col in ['Medicine_Name', 'Medicine_Composition', 'Medicine_Description']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    print(f"Cleaned medicine dataset: {df_clean.shape}")
    return df_clean

if __name__ == '__main__':
    clean_medicine_data()
