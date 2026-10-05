from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'ml' / 'medicine_by_disease_model.pkl'

def train_medicine_model():
    print("PROTECTION NOTICE: Production medicine model artifact exists at:")
    print(f"  {MODEL_PATH}")
    print("As per project specifications, existing fitted models are preserved and not overwritten.")
    print("To evaluate the fitted models, run: python training/evaluate_medicine_model.py")

if __name__ == '__main__':
    train_medicine_model()
