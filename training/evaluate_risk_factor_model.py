import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'disease_risk_model.pkl'
FEATURES_PATH = BASE_DIR / 'datasets' / 'processed' / 'risk_factor_features.csv'

def evaluate_risk_factor_model():
    """
    Evaluates real fitted disease risk model against processed risk features.
    """
    if not MODEL_PATH.exists() or not FEATURES_PATH.exists():
        print("Required artifacts or datasets not found.")
        return

    drm = joblib.load(MODEL_PATH)
    model = drm['model']
    vectorizer = drm['vectorizer']
    disease_names = drm['disease_names']

    df = pd.read_csv(FEATURES_PATH)
    print(f"Loaded processed risk factor features: {df.shape}")

    matched_count = 0
    total = len(df)

    for _, row in df.iterrows():
        dname = str(row['DNAME']).strip()
        X = vectorizer.transform([dname])
        distances, indices = model.kneighbors(X, n_neighbors=1)
        matched_disease = disease_names[indices[0][0]]
        
        if matched_disease.lower() == dname.lower():
            matched_count += 1

    print(f"\n--- Risk Factor NearestNeighbors Precision ---")
    print(f"Exact Profile Retrieval Rate: {matched_count / total * 100:.2f}% ({matched_count}/{total} diseases)")

if __name__ == '__main__':
    evaluate_risk_factor_model()
