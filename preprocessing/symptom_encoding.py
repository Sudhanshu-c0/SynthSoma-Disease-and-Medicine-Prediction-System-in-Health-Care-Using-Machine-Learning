from utils.symptom_mapper import map_user_input_to_features, normalize_symptom_name

def encode_symptoms_list(raw_symptoms, feature_names):
    return map_user_input_to_features(raw_symptoms, feature_names)
