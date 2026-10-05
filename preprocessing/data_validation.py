from utils.model_loader import get_model_loader

def validate_clinical_inputs(module_type, inputs):
    """
    Validates clinical inputs for each of the four modules against fitted metadata.
    """
    loader = get_model_loader()
    
    if module_type == 'disease':
        symptom_space = loader.get_disease_symptoms()
        valid = [s for s in inputs if s in symptom_space]
        return len(valid) > 0, valid
        
    elif module_type == 'medicine':
        known = [d.lower() for d in loader.get_medicine_diseases()]
        return bool(inputs and str(inputs).strip().lower() in known or len(str(inputs).strip()) >= 2), inputs
        
    elif module_type == 'precaution':
        known = [d.lower() for d in loader.get_precaution_diseases()]
        return bool(inputs and len(str(inputs).strip()) >= 2), inputs
        
    elif module_type == 'risk_factor':
        known = [d.lower() for d in loader.get_risk_diseases()]
        return bool(inputs and len(str(inputs).strip()) >= 2), inputs
        
    return False, None
