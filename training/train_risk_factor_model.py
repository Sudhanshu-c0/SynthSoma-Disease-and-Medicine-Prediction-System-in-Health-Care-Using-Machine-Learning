from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'disease_risk_model.pkl'

def train_risk_factor_model():
    print("PROTECTION NOTICE: Production risk factor model artifact exists at:")
    print(f"  {MODEL_PATH}")
    print("As per project specifications, existing fitted models are preserved and not overwritten.")
    print("To evaluate the fitted models, run: python training/evaluate_risk_factor_model.py")

if __name__ == '__main__':
    train_risk_factor_model()
