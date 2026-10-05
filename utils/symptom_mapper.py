from utils.model_loader import get_model_loader

def format_symptom_display(feature_name):
    """Convert 'abdominal_pain' to 'Abdominal Pain'"""
    return feature_name.replace('_', ' ').title()

def get_formatted_symptoms():
    loader = get_model_loader()
    raw_symptoms = loader.get_disease_symptoms()
    formatted = []
    for s in raw_symptoms:
        formatted.append({
            'code': s,
            'name': format_symptom_display(s)
        })
    # Sort alphabetically by display name
    return sorted(formatted, key=lambda x: x['name'])

def normalize_symptom_name(user_text):
    """Normalize user input to match model feature name."""
    clean = user_text.strip().lower().replace('-', '_').replace(' ', '_')
    return clean

def map_user_input_to_features(input_list, known_features):
    """Takes user inputs (e.g. 'Abdominal pain', 'stomach ache', 'vomiting')
    and maps them to known 131 symptom feature strings."""
    matched = []
    known_set = set(known_features)
    
    # Common synonyms/aliases mapping to actual features
    aliases = {
        'stomach_pain': 'abdominal_pain',
        'stomach_ache': 'abdominal_pain',
        'belly_ache': 'belly_pain',
        'fever': 'high_fever',
        'temperature': 'high_fever',
        'loose_motion': 'diarrhoea',
        'loose_motions': 'diarrhoea',
        'rash': 'skin_rash',
        'rashes': 'skin_rash',
        'cold': 'continuous_sneezing',
        'sneezing': 'continuous_sneezing',
        'tiredness': 'fatigue',
        'weakness': 'fatigue',
        'head_pain': 'headache',
        'puke': 'vomiting',
        'throwing_up': 'vomiting',
        'breathlessness': 'breathlessness',
        'shortness_of_breath': 'breathlessness',
        'yellow_skin': 'yellowish_skin',
        'yellow_eyes': 'yellowing_of_eyes',
    }

    for item in input_list:
        norm = normalize_symptom_name(item)
        if norm in known_set:
            matched.append(norm)
        elif norm in aliases and aliases[norm] in known_set:
            matched.append(aliases[norm])
        else:
            # Substring matching fallback
            for k in known_features:
                if norm in k or k in norm:
                    matched.append(k)
                    break
                    
    # Return unique preserved order
    return list(dict.fromkeys(matched))
