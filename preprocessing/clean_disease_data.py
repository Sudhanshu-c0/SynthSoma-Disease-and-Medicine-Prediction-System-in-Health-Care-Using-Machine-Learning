import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / 'datasets' / 'raw' / 'disease_symptoms.csv'
CLEANED_PATH = BASE_DIR / 'datasets' / 'cleaned' / 'disease_information_cleaned.csv'
PROCESSED_PATH = BASE_DIR / 'datasets' / 'processed' / 'disease_features.csv'

def clean_disease_data():
    """
    Cleans raw disease symptoms dataset and extracts symptom features.
    """
    if not RAW_PATH.exists():
        print(f"Raw disease symptoms dataset not found at {RAW_PATH}")
        return None

    df_raw = pd.read_csv(RAW_PATH, encoding='utf-8')
    print(f"Loaded raw disease symptoms: {df_raw.shape}")
    
    # Strip whitespace from symptom strings
    symptom_cols = [c for c in df_raw.columns if c.startswith('Symptom')]
    for col in symptom_cols:
        df_raw[col] = df_raw[col].astype(str).str.strip().str.lower()
        df_raw.loc[df_raw[col] == 'nan', col] = None

    return df_raw

if __name__ == '__main__':
    clean_disease_data()
