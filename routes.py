from bottle import route, view, request, redirect, response, template, static_file
from datetime import datetime
import os

from services.user_service import register_user, authenticate_user
from services.validation import validate_form
from services.file_service import save_json, load_json
from services.new_products_logic import load_news, save_news,validate_news_form

DATA_FILE = 'static/resources/partners.json'
USERS_FILE = 'static/resources/users.json'
UPLOAD_DIR = 'static/resources/logos'
os.makedirs(UPLOAD_DIR, exist_ok=True)

companies = load_json(DATA_FILE) or []
users = load_json(USERS_FILE) or []

@route('/')
@route('/home')
@view('index')
def home():
    return dict(year=datetime.now().year)

@route('/constructor')
@view('constructor')
def constructor():
    return dict(title='PC Builder', year=datetime.now().year)

@route('/profile')
@view('profile')
def profile():
    return dict(title='Profile settings',
                message='You can change your profile here.',
                year=datetime.now().year)

@route('/auth')
@view('auth')
def auth():
    return dict(title='Login / Register',
                message='Welcome to the Authorization Page',
                year=datetime.now().year,
                error=None)

@route('/register', method='POST')
def register():
    username = request.forms.get('username').strip()
    password = request.forms.get('password').strip()
    firstname = request.forms.get('firstname', '').strip()
    lastname = request.forms.get('lastname', '').strip()
    email = request.forms.get('email', '').strip()
    phone = request.forms.get('phone', '').strip()
    birthdate = request.forms.get('birthdate', '').strip()

    error = register_user(
        username, password,
        firstname=firstname, lastname=lastname,
        email=email, phone=phone, birthdate=birthdate,
        users_file=USERS_FILE
    )
    if error:
        return template('auth', title='Login / Register',
                        message='Welcome to the Authorization Page',
                        year=datetime.now().year, error=error)

    response.set_cookie('username', username, secret='some-secret-key')
    redirect('/home')

@route('/login', method='POST')
def login():
    username = request.forms.get('username').strip()
    password = request.forms.get('password').strip()

    if authenticate_user(username, password, USERS_FILE):
        response.set_cookie('username', username, secret='some-secret-key')
        redirect('/home')
    else:
        return template('auth', title='Login / Register',
                        message='Welcome to the Authorization Page',
                        year=datetime.now().year, error='Invalid username or password')

@route('/logout')
def logout():
    response.delete_cookie('username')
    redirect('/auth')

@route('/partners')
@view('partner')
def show_partners():
    global companies
    companies = load_json(DATA_FILE) or []
    return dict(title="Partner Companies",
                year=datetime.now().year,
                companies=companies,
                form_data={},
                errors={})

@route('/add', method='POST')
def add_partner():
    global companies
    form_data = {
        'name': request.forms.get('name', '').strip(),
        'description': request.forms.get('description', '').strip(),
        'phone': request.forms.get('phone', '').strip(),
        'date': request.forms.get('date', '').strip(),
    }

    logo = request.files.get('logo')
    filename = None

    if logo and logo.filename:
        name, ext = os.path.splitext(logo.filename.lower())
        if ext not in ('.png', '.jpg', '.jpeg'):
            return template('partner', title="Partner Companies", year=datetime.now().year,
                            companies=companies, form_data=form_data,
                            errors={'logo': 'Invalid image format'})
        filename = f"{logo.filename}"
        logo.save(os.path.join(UPLOAD_DIR, filename))

    errors = validate_form(form_data)
    if errors:
        return template('partner', title="Partner Companies", year=datetime.now().year,
                        companies=companies, form_data=form_data, errors=errors)

    form_data['logo'] = filename if filename else ''
    companies.append(form_data)
    save_json(DATA_FILE, companies)

    redirect('/partners')
    
@route('/new_products', method=['GET', 'POST'])
def new_products():
    author = request.forms.get('author', '').strip()
    text = request.forms.get('text', '').strip()
    date = request.forms.get('date', '').strip()

    if request.method == 'POST':
        errors = validate_news_form(author, text, date)

        if not errors:
            news_list = load_news()
            news_list.insert(0, {'author': author, 'text': text, 'date': date})
            save_news(news_list)
            return redirect('/new_products')
        else:
            return template('new_products.tpl',
                            new_products=load_news(),
                            error="Пожалуйста, исправьте ошибки в форме.",
                            errors=errors,
                            author=author,
                            text=text,
                            date=date,
                            year=datetime.now().year)

    return template('new_products.tpl',
                    new_products=load_news(),
                    error=None,
                    errors={},
                    author='',
                    text='',
                    date='',
                    year=datetime.now().year)


@route('/logos/<filename>')
def serve_logo(filename):
    return static_file(filename, root=UPLOAD_DIR)