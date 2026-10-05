import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'medicine_by_disease_model.pkl'
FEATURES_PATH = BASE_DIR / 'datasets' / 'processed' / 'medicine_features.csv'

def evaluate_medicine_model():
    """
    Evaluates real fitted medicine model against processed medicine dataset.
    """
    if not MODEL_PATH.exists() or not FEATURES_PATH.exists():
        print("Required artifacts or datasets not found.")
        return

    mbd = joblib.load(MODEL_PATH)
    model = mbd['model']
    vectorizer = mbd['vectorizer']
    binarizer = mbd['binarizer']

    df = pd.read_csv(FEATURES_PATH)
    print(f"Loaded processed medicine features: {df.shape}")

    correct = 0
    total = len(df)

    for _, row in df.iterrows():
        dname = str(row['Disease_Name'])
        X = vectorizer.transform([dname])
        pred = model.predict(X)
        pred_meds = set(binarizer.inverse_transform(pred)[0])
        
        expected_raw = str(row['Medicine_List_Joined']).split(';')
        expected = set([m.strip() for m in expected_raw if m.strip()])
        
        # Check if intersection exists
        if pred_meds & expected:
            correct += 1

    print(f"\n--- Medicine Model Accuracy ---")
    print(f"Match Rate (Top overlap): {correct / total * 100:.2f}% ({correct}/{total} conditions matched)")

if __name__ == '__main__':
    evaluate_medicine_model()
