import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'disease_precaution_model.pkl'
FEATURES_PATH = BASE_DIR / 'datasets' / 'processed' / 'precaution_features.csv'

def evaluate_precaution_model():
    """
    Evaluates real fitted precaution model against processed precaution dataset.
    """
    if not MODEL_PATH.exists() or not FEATURES_PATH.exists():
        print("Required artifacts or datasets not found.")
        return

    dpm = joblib.load(MODEL_PATH)
    model = dpm['model']
    vectorizer = dpm['vectorizer']
    binarizer = dpm['binarizer']

    df = pd.read_csv(FEATURES_PATH)
    print(f"Loaded processed precaution features: {df.shape}")

    correct = 0
    total = len(df)

    for _, row in df.iterrows():
        dname = str(row['Disease'])
        X = vectorizer.transform([dname])
        pred = model.predict(X)
        pred_precs = set(binarizer.inverse_transform(pred)[0])
        
        expected_raw = str(row['Precautions_Joined']).split(';')
        expected = set([p.strip().lower() for p in expected_raw if p.strip()])
        
        if pred_precs & expected:
            correct += 1

    print(f"\n--- Precaution Model Accuracy ---")
    print(f"Match Rate (Top overlap): {correct / total * 100:.2f}% ({correct}/{total} conditions matched)")

if __name__ == '__main__':
    evaluate_precaution_model()
