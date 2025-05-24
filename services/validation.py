import re
from datetime import datetime

def validate_partner_form(form_data):
    """
    Validate form data for adding a new partner.
    Args:
        form_data: Dictionary containing form fields (name, description, phone, date).
    Returns:
        Dictionary of errors (empty if no errors).
    """
    errors = {}

    # Validate name: non-empty, 3-100 characters, letters, numbers, spaces, and basic punctuation
    name = form_data.get('name', '').strip()
    if not name:
        errors['name'] = 'Company name is required.'
    elif len(name) < 3:
        errors['name'] = 'Company name must be at least 3 characters.'
    elif len(name) > 100:
        errors['name'] = 'Company name cannot exceed 100 characters.'
    elif not re.match(r'^[A-Za-z0-9\s.,&()-]+$', name):
        errors['name'] = 'Name can only contain letters, numbers, spaces, and basic punctuation.'

    # Validate description: non-empty, 10-500 characters
    description = form_data.get('description', '').strip()
    if not description:
        errors['description'] = 'Description is required.'
    elif len(description) < 10:
        errors['description'] = 'Description must be at least 10 characters.'
    elif len(description) > 500:
        errors['description'] = 'Description cannot exceed 500 characters.'

    # Validate phone: matches +7(XXX)XXX-XX-XX format
    phone = form_data.get('phone', '').strip()
    phone_pattern = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'
    if not phone:
        errors['phone'] = 'Phone number is required.'
    elif not re.match(phone_pattern, phone):
        errors['phone'] = 'Phone must be in format +7(XXX)XXX-XX-XX.'

    # Validate date: non-empty, valid date, not in future
    date_str = form_data.get('date', '').strip()
    if not date_str:
        errors['date'] = 'Date is required.'
    else:
        try:
            input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            current_date = datetime.now().date()
            if input_date > current_date:
                errors['date'] = 'Date cannot be in the future.'
        except ValueError:
            errors['date'] = 'Invalid date format.'

    return errors

def validate_registration_form(form_data):
    """
    Validate form data for user registration.
    Args:
        form_data: Dictionary containing form fields (username, password, firstname, lastname, email, phone, birthdate).
    Returns:
        Dictionary of errors (empty if no errors).
    """
    errors = {}

    # Validate username: non-empty, letters and numbers only
    username = form_data.get('username', '').strip()
    if not username:
        errors['username'] = 'Username is required.'
    elif not re.match(r'^[A-Za-z0-9]+$', username):
        errors['username'] = 'Username can only contain letters and numbers.'

    # Validate password: non-empty, at least 6 characters
    password = form_data.get('password', '').strip()
    if not password:
        errors['password'] = 'Password is required.'
    elif len(password) < 6:
        errors['password'] = 'Password must be at least 6 characters.'

    # Validate firstname: letters, spaces, and hyphens if provided
    firstname = form_data.get('firstname', '').strip()
    if firstname and not re.match(r'^[A-Za-z\s-]+$', firstname):
        errors['firstname'] = 'First name can only contain letters, spaces, and hyphens.'

    # Validate lastname: letters, spaces, and hyphens if provided
    lastname = form_data.get('lastname', '').strip()
    if lastname and not re.match(r'^[A-Za-z\s-]+$', lastname):
        errors['lastname'] = 'Last name can only contain letters, spaces, and hyphens.'

    # Validate email: valid format if provided
    email = form_data.get('email', '').strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if email and not re.match(email_pattern, email):
        errors['email'] = 'Invalid email format.'

    # Validate phone: matches +7(XXX)XXX-XX-XX format, required
    phone = form_data.get('phone', '').strip()
    phone_pattern = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'
    if not phone:
        errors['phone'] = 'Phone number is required.'
    elif not re.match(phone_pattern, phone):
        errors['phone'] = 'Phone must be in format +7(XXX)XXX-XX-XX.'

    # Validate birthdate: valid date, not in future, required
    birthdate = form_data.get('birthdate', '').strip()
    if not birthdate:
        errors['birthdate'] = 'Invalid birthdate format.'
    else:
        try:
            input_date = datetime.strptime(birthdate, '%Y-%m-%d').date()
            current_date = datetime.now().date()
            if input_date > current_date:
                errors['birthdate'] = 'Birthdate cannot be in the future.'
        except ValueError:
            errors['birthdate'] = 'Invalid birthdate format.'

    return errors

def validate_login_form(form_data):
    """
    Validate form data for user login.
    Args:
        form_data: Dictionary containing form fields (username, password).
    Returns:
        Dictionary of errors (empty if no errors).
    """
    errors = {}

    # Validate username: non-empty, letters and numbers only
    username = form_data.get('username', '').strip()
    if not username:
        errors['username'] = 'Username is required.'
    elif not re.match(r'^[A-Za-z0-9]+$', username):
        errors['username'] = 'Username can only contain letters and numbers.'

    # Validate password: non-empty, at least 6 characters
    password = form_data.get('password', '').strip()
    if not password:
        errors['password'] = 'Password is required.'
    elif len(password) < 6:
        errors['password'] = 'Password must be at least 6 characters.'

    return errors