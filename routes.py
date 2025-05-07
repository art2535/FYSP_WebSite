"""
Routes and views for the Bottle application.
"""

import os
import re
import json
from datetime import datetime
from bottle import route, view, request, redirect, response, template, static_file

# Paths for data and logos
UPLOAD_DIR = 'static/resources/logos'
DATA_FILE = 'static/resources/partners.json'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load data on startup
companies = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        companies = json.load(f)

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(year=datetime.now().year)

@route('/auth')
@view('auth')
def auth():
    """Login / Registration page."""
    return dict(
        title='Login / Register',
        message='Welcome to the Authorization Page',
        year=datetime.now().year,
        error=None
    )

@route('/register', method='POST')
def do_register():
    """Handle registration."""
    username = request.forms.get('username')
    password = request.forms.get('password')
    if not username or not password:
        return template('auth', title='Login / Register', message='Welcome to the Authorization Page', 
                        year=datetime.now().year, error='Username and password are required')
    response.set_cookie('username', username, secret='some-secret-key')
    redirect('/home')

@route('/login', method='POST')
def do_login():
    """Handle login."""
    username = request.forms.get('username')
    password = request.forms.get('password')
    if not username or not password:
        return template('auth', title='Login / Register', message='Welcome to the Authorization Page', 
                        year=datetime.now().year, error='Username and password are required')
    response.set_cookie('username', username, secret='some-secret-key')
    redirect('/home')

@route('/logout')
def logout():
    """Log out the user."""
    response.delete_cookie('username')
    redirect('/auth')

@route('/constructor')
@view('constructor')
def constructor():
    """PC Builder page."""
    return dict(
        title='PC Builder',
        year=datetime.now().year
    )

@route('/profile')
@view('profile')
def profile():
    """User profile settings."""
    return dict(
        title='Profile settings',
        message='You can change your profile here.',
        year=datetime.now().year,
    )

@route('/partners')
@view('partner')
def show_partners():
    """Display partner companies."""
    return dict(
        title="Partner Companies",
        year=datetime.now().year,
        companies=companies,
        form_data={},
        errors={}
    )

@route('/add', method='POST')
def add_partner():
    """Add a partner company."""
    form_data = {
        'name': request.forms.get('name', '').strip(),
        'description': request.forms.get('description', '').strip(),
        'phone': request.forms.get('phone', '').strip(),
        'date': request.forms.get('date', '').strip(),
    }

    logo = request.files.get('logo')
    filename = None

    # Check and save logo
    if logo and logo.filename:
        name, ext = os.path.splitext(logo.filename.lower())
        if ext not in ('.png', '.jpg', '.jpeg'):
            return template('partner',
                            title="Partner Companies",
                            year=datetime.now().year,
                            companies=companies,
                            form_data=form_data,
                            errors={'logo': 'Invalid image format'})
        filename = f"{logo.filename}"
        logo.save(os.path.join(UPLOAD_DIR, filename))

    errors = validate_form(form_data)
    if errors:
        return template('partner',
                        title="Partner Companies",
                        year=datetime.now().year,
                        companies=companies,
                        form_data=form_data,
                        errors=errors)

    form_data['logo'] = filename if filename else ''
    companies.append(form_data)

    # Save to file
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=4)

    redirect('/partners')

@route('/logos/<filename>')
def serve_logo(filename):
    """Serve the logo by filename."""
    return static_file(filename, root=UPLOAD_DIR)

def validate_form(data):
    """Validate form data."""
    errors = {}

    if not data.get('name'):
        errors['name'] = 'Enter the company name.'

    if not data.get('description'):
        errors['description'] = 'Enter a description.'

    phone = data.get('phone', '')
    phone_pattern = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'
    if not re.match(phone_pattern, phone):
        errors['phone'] = 'Phone must be in the format +7(XXX)XXX-XX-XX.'

    date_str = data.get('date', '')
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        if date_obj > datetime.now().date():
            errors['date'] = 'Date cannot be in the future.'
    except ValueError:
        errors['date'] = 'Invalid date format.'

    return errors