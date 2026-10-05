import joblib
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'complete_disease_system.pkl'
FEATURES_PATH = BASE_DIR / 'datasets' / 'processed' / 'disease_features.csv'

def evaluate_disease_model():
    """
    Evaluates the trained disease models on the processed disease features.
    """
    if not MODEL_PATH.exists() or not FEATURES_PATH.exists():
        print("Required artifacts or datasets not found.")
        return

    system = joblib.load(MODEL_PATH)
    models = system.get('models', {})
    symptom_features = system.get('symptom_features', [])
    label_encoder = system.get('label_encoder')

    df = pd.read_csv(FEATURES_PATH)
    print(f"Loaded processed test dataset: {df.shape}")

    # Build matrix for available features
    X = np.zeros((len(df), len(symptom_features)), dtype=np.float32)
    for col_idx, feat in enumerate(symptom_features):
        if feat in df.columns:
            X[:, col_idx] = df[feat].values

    y_raw = df['Disease'].str.lower().str.strip()
    y_encoded = label_encoder.transform(y_raw)

    print("\n--- Model Benchmark on Processed Disease Dataset ---")
    for name, clf in models.items():
        try:
            preds = clf.predict(X)
            acc = np.mean(preds == y_encoded)
            print(f"Model: {name:32s} | Top-1 Accuracy: {acc * 100:.2f}%")
        except Exception as e:
            print(f"Model: {name:32s} | Evaluation note: {e}")

if __name__ == '__main__':
    evaluate_disease_model()
