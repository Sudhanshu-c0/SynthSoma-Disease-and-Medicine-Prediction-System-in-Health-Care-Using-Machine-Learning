import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'complete_disease_system.pkl'

def train_disease_model():
    print("PROTECTION NOTICE: Production disease model artifact exists at:")
    print(f"  {MODEL_PATH}")
    print("As per project specifications, existing fitted models are preserved and not overwritten.")
    print("To evaluate the fitted models, run: python training/evaluate_disease_model.py")

if __name__ == '__main__':
    train_disease_model()
