import re

def validate_signup_form(data):
    errors = {}
    
    name = (data.get('name') or '').strip()
    user_id = (data.get('user_id') or '').strip()
    email = (data.get('email') or '').strip().lower()
    phone = (data.get('phone') or '').strip()
    location = (data.get('location') or '').strip()
    password = data.get('password') or ''
    confirm_password = data.get('confirm_password') or ''
    
    # Name validation
    if not name:
        errors['name'] = 'Full name is required.'
    elif len(name) < 2:
        errors['name'] = 'Full name must be at least 2 characters.'

    # User ID validation
    if not user_id:
        errors['user_id'] = 'User ID is required.'
    elif len(user_id) < 3:
        errors['user_id'] = 'User ID must be at least 3 characters.'
    elif not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        errors['user_id'] = 'User ID can only contain letters, numbers, hyphens, and underscores.'

    # Email validation
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not email:
        errors['email'] = 'Email address is required.'
    elif not re.match(email_regex, email):
        errors['email'] = 'Please enter a valid email address.'

    # Phone validation
    phone_clean = re.sub(r'[\s\-\(\)\+]', '', phone)
    if not phone:
        errors['phone'] = 'Phone number is required.'
    elif len(phone_clean) < 7 or len(phone_clean) > 15 or not phone_clean.isdigit():
        errors['phone'] = 'Please enter a valid phone number (7 to 15 digits).'

    # Location validation
    if not location:
        errors['location'] = 'Location / City is required.'

    # Password validation
    if not password:
        errors['password'] = 'Password is required.'
    elif len(password) < 6:
        errors['password'] = 'Password must be at least 6 characters long.'
        
    if password != confirm_password:
        errors['confirm_password'] = 'Passwords do not match.'

    return len(errors) == 0, errors

def validate_login_form(data):
    errors = {}
    username_or_email = (data.get('username') or data.get('email') or '').strip()
    password = data.get('password') or ''
    
    if not username_or_email:
        errors['username'] = 'User ID or Email is required.'
    if not password:
        errors['password'] = 'Password is required.'
        
    return len(errors) == 0, errors

def validate_symptoms_input(symptoms, available_symptoms):
    if not symptoms:
        return False, "Please select or enter at least one symptom."
    
    if isinstance(symptoms, str):
        # Support comma separated string or single symptom
        symptoms = [s.strip().lower().replace(' ', '_') for s in symptoms.split(',') if s.strip()]
    elif isinstance(symptoms, list):
        symptoms = [str(s).strip().lower().replace(' ', '_') for s in symptoms if str(s).strip()]
        
    valid_selected = [s for s in symptoms if s in available_symptoms]
    if not valid_selected:
        return False, f"None of the provided symptoms match the system's recognized feature space. Recognized examples: {', '.join(available_symptoms[:5])}."
        
    return True, valid_selected

def validate_disease_input(disease_name):
    if not disease_name or not str(disease_name).strip():
        return False, "Please enter or select a disease name."
    cleaned = str(disease_name).strip()
    if len(cleaned) < 2:
        return False, "Disease name must be at least 2 characters."
    return True, cleaned
