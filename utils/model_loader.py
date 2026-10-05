import os
import joblib
import pandas as pd
from pathlib import Path
from flask import current_app

class ModelLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.base_dir = Path(__file__).resolve().parent.parent
        self.models_dir = self.base_dir / 'models' / 'ml'
        self.cleaned_dir = self.base_dir / 'datasets' / 'cleaned'
        self.raw_dir = self.base_dir / 'datasets' / 'raw'
        
        # ML Artifacts
        self.disease_system = None
        self.disease_encoder = None
        self.medicine_model = None
        self.medicine_encoder = None
        self.precaution_model = None
        self.precaution_encoder = None
        self.risk_model = None
        self.risk_encoder = None
        
        # Datasets & Lookup Dictionaries
        self.disease_info_df = None
        self.medicine_df = None
        self.precaution_df = None
        
        self.load_artifacts()
        self.load_datasets()
        self._initialized = True

    def load_artifacts(self):
        try:
            cds_path = self.models_dir / 'complete_disease_system.pkl'
            if cds_path.exists():
                self.disease_system = joblib.load(cds_path)
        except Exception as e:
            print(f"Warning: Failed loading complete_disease_system.pkl: {e}")

        try:
            dse_path = self.models_dir / 'disease_system_encoder.pkl'
            if dse_path.exists():
                self.disease_encoder = joblib.load(dse_path)
        except Exception as e:
            print(f"Warning: Failed loading disease_system_encoder.pkl: {e}")

        try:
            mbd_path = self.models_dir / 'medicine_by_disease_model.pkl'
            if mbd_path.exists():
                self.medicine_model = joblib.load(mbd_path)
        except Exception as e:
            print(f"Warning: Failed loading medicine_by_disease_model.pkl: {e}")

        try:
            me_path = self.models_dir / 'medicine_encoder.pkl'
            if me_path.exists():
                self.medicine_encoder = joblib.load(me_path)
        except Exception as e:
            print(f"Warning: Failed loading medicine_encoder.pkl: {e}")

        try:
            dpm_path = self.models_dir / 'disease_precaution_model.pkl'
            if dpm_path.exists():
                self.precaution_model = joblib.load(dpm_path)
        except Exception as e:
            print(f"Warning: Failed loading disease_precaution_model.pkl: {e}")

        try:
            pe_path = self.models_dir / 'precaution_encoder.pkl'
            if pe_path.exists():
                self.precaution_encoder = joblib.load(pe_path)
        except Exception as e:
            print(f"Warning: Failed loading precaution_encoder.pkl: {e}")

        try:
            drm_path = self.models_dir / 'disease_risk_model.pkl'
            if drm_path.exists():
                self.risk_model = joblib.load(drm_path)
        except Exception as e:
            print(f"Warning: Failed loading disease_risk_model.pkl: {e}")

        try:
            dre_path = self.models_dir / 'disease_risk_encoder.pkl'
            if dre_path.exists():
                self.risk_encoder = joblib.load(dre_path)
        except Exception as e:
            print(f"Warning: Failed loading disease_risk_encoder.pkl: {e}")

    def load_datasets(self):
        # Load cleaned datasets with fallback to raw
        try:
            path = self.cleaned_dir / 'disease_information_cleaned.csv'
            if path.exists():
                self.disease_info_df = pd.read_csv(path, encoding='utf-8')
            else:
                self.disease_info_df = pd.read_csv(self.raw_dir / 'disease_riskFactors.csv', encoding='latin1')
        except Exception as e:
            print(f"Warning loading disease info dataset: {e}")

        try:
            path = self.cleaned_dir / 'medicine_prediction_cleaned.csv'
            if path.exists():
                self.medicine_df = pd.read_csv(path, encoding='utf-8')
            else:
                self.medicine_df = pd.read_csv(self.raw_dir / 'disease_medicine.csv', encoding='latin1')
        except Exception as e:
            print(f"Warning loading medicine dataset: {e}")

        try:
            path = self.cleaned_dir / 'precaution_cleaned.csv'
            if path.exists():
                self.precaution_df = pd.read_csv(path, encoding='utf-8')
            else:
                self.precaution_df = pd.read_csv(self.raw_dir / 'disease_precaution.csv', encoding='utf-8')
        except Exception as e:
            print(f"Warning loading precaution dataset: {e}")

    # Accessors
    def get_disease_symptoms(self):
        if self.disease_system and 'symptom_features' in self.disease_system:
            return self.disease_system['symptom_features']
        if self.disease_encoder and 'symptom_features' in self.disease_encoder:
            return self.disease_encoder['symptom_features']
        return []

    def get_disease_names(self):
        if self.disease_system and 'disease_names' in self.disease_system:
            return [str(d) for d in self.disease_system['disease_names']]
        if self.disease_encoder and 'disease_names' in self.disease_encoder:
            return [str(d) for d in self.disease_encoder['disease_names']]
        return []

    def get_available_disease_classifiers(self):
        if self.disease_system and 'models' in self.disease_system:
            return list(self.disease_system['models'].keys())
        return []

    def get_default_disease_classifier(self):
        if self.disease_system and 'default_model' in self.disease_system:
            return self.disease_system['default_model']
        return 'K-Nearest Neighbors (Cosine)'

    def get_medicine_diseases(self):
        if self.medicine_model and 'known_diseases' in self.medicine_model:
            return [str(d) for d in self.medicine_model['known_diseases']]
        if self.medicine_encoder and 'known_diseases' in self.medicine_encoder:
            return [str(d) for d in self.medicine_encoder['known_diseases']]
        return []

    def get_precaution_diseases(self):
        if self.precaution_model and 'known_diseases' in self.precaution_model:
            return [str(d) for d in self.precaution_model['known_diseases']]
        if self.precaution_encoder and 'known_diseases' in self.precaution_encoder:
            return [str(d) for d in self.precaution_encoder['known_diseases']]
        return []

    def get_risk_diseases(self):
        if self.risk_model and 'disease_names' in self.risk_model:
            return [str(d) for d in self.risk_model['disease_names']]
        if self.risk_encoder and 'disease_names' in self.risk_encoder:
            return [str(d) for d in self.risk_encoder['disease_names']]
        return []

# Singleton accessor
_loader_instance = None

def get_model_loader():
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = ModelLoader()
    return _loader_instance
