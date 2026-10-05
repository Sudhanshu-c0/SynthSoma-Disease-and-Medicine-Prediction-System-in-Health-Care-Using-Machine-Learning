import numpy as np

def build_disease_feature_vector(active_symptoms, symptom_feature_names):
    """
    Constructs a 1xN binary numpy feature vector matching the exact feature ordering.
    """
    vector = np.zeros((1, len(symptom_feature_names)), dtype=np.float32)
    name_to_idx = {name: i for i, name in enumerate(symptom_feature_names)}
    
    for s in active_symptoms:
        if s in name_to_idx:
            vector[0, name_to_idx[s]] = 1.0
            
    return vector
