from services.file_service import load_json, save_json
from services.validation import validate_registration_form, validate_login_form

def register_user(form_data, data_file):
    """
    Register a new user.
    Args:
        form_data: Form data from request.forms
        data_file: Path to users JSON file
    Returns:
        Dictionary with username or error
    """
    errors = validate_registration_form(form_data)
    if errors:
        return {'error': 'Please fix the errors in the form.', 'errors': errors}

    users = load_json(data_file) or []
    username = form_data.get('username', '').strip()
    if any(user['username'] == username for user in users):
        return {'error': 'Username already exists.', 'errors': {'username': 'Username already exists.'}}

    user_data = {
        'username': username,
        'password': form_data.get('password', '').strip(),
        'firstname': form_data.get('firstname', '').strip(),
        'lastname': form_data.get('lastname', '').strip(),
        'email': form_data.get('email', '').strip(),
        'phone': form_data.get('phone', '').strip(),
        'birthdate': form_data.get('birthdate', '').strip()
    }
    users.append(user_data)
    save_json(data_file, users)
    return {'username': username, 'error': None, 'errors': {}}

def authenticate_user(username, password, data_file):
    """
    Authenticate a user.
    Args:
        username: Username from form
        password: Password from form
        data_file: Path to users JSON file
    Returns:
        Dictionary with success status and username
    """
    form_data = {'username': username, 'password': password}
    errors = validate_login_form(form_data)
    if errors:
        return {'success': False, 'error': 'Please fix the errors in the form.', 'errors': errors}

    users = load_json(data_file) or []
    for user in users:
        if user['username'] == username and user['password'] == password:
            return {'success': True, 'username': username, 'error': None, 'errors': {}}
    return {'success': False, 'error': 'Invalid username or password', 'errors': {'username': 'Invalid username or password'}}

def logout_user():
    """
    Clear user session (cookie handled in routes).
    """
    pass