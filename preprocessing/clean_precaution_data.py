import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / 'datasets' / 'raw' / 'disease_precaution.csv'
CLEANED_PATH = BASE_DIR / 'datasets' / 'cleaned' / 'precaution_cleaned.csv'

def clean_precaution_data():
    """
    Cleans raw disease precaution dataset.
    """
    if not RAW_PATH.exists():
        print(f"Raw precaution dataset not found at {RAW_PATH}")
        return None

    df_raw = pd.read_csv(RAW_PATH, encoding='utf-8')
    for col in df_raw.columns:
        df_raw[col] = df_raw[col].astype(str).str.strip().str.lower()
        df_raw.loc[df_raw[col] == 'nan', col] = None

    print(f"Cleaned precaution dataset: {df_raw.shape}")
    return df_raw

if __name__ == '__main__':
    clean_precaution_data()
