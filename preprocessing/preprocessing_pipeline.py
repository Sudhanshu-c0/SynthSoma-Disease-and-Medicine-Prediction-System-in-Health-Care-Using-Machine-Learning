from preprocessing.clean_disease_data import clean_disease_data
from preprocessing.clean_medicine_data import clean_medicine_data
from preprocessing.clean_precaution_data import clean_precaution_data
from preprocessing.clean_risk_factor_data import clean_risk_factor_data

def run_pipeline():
    print("Running SynthSoma data preprocessing pipeline...")
    d_clean = clean_disease_data()
    m_clean = clean_medicine_data()
    p_clean = clean_precaution_data()
    r_clean = clean_risk_factor_data()
    print("Pipeline run completed without modifying raw datasets.")

if __name__ == '__main__':
    run_pipeline()
