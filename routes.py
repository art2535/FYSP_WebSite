from bottle import route, view, request, redirect, response, template, static_file
from datetime import datetime

from services.partner_service import get_partners, add_partners
from services.user_service import register_user, authenticate_user, logout_user
from services.new_products_logic import load_news, save_news, validate_news_form

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
                error=None,
                errors={},
                form_data={},
                login_form_data={})

@route('/register', method='POST')
def register():
    result = register_user(request.forms, 'static/resources/users.json')
    if result.get('error'):
        return template('auth',
                       title='Login / Register',
                       message='Welcome to the Authorization Page',
                       year=datetime.now().year,
                       error=result['error'],
                       errors=result.get('errors', {}),
                       form_data=dict(request.forms),
                       login_form_data={})
    response.set_cookie('username', result['username'], secret='some-secret-key')
    redirect('/home')

@route('/login', method='POST')
def login():
    username = request.forms.get('username', '').strip()
    result = authenticate_user(username,
                              request.forms.get('password', '').strip(),
                              'static/resources/users.json')
    if not result['success']:
        return template('auth',
                       title='Login / Register',
                       message='Welcome to the Authorization Page',
                       year=datetime.now().year,
                       error=None,
                       errors={},
                       form_data={},
                       login_form_data={'username': username, 'error': result.get('error', 'Invalid username or password')})
    response.set_cookie('username', result['username'], secret='some-secret-key')
    redirect('/home')

@route('/logout')
def logout():
    logout_user()
    redirect('/auth')

@route('/partners')
@view('partner')
def show_partners():
    partners_data = get_partners('static/resources/partners.json')
    return dict(title="Partner Companies",
                year=datetime.now().year,
                companies=partners_data['companies'],
                form_data={},
                errors={})

@route('/add', method='POST')
def add_partner():
    result = add_partners(request.forms, request.files.get('logo'), 'static/resources/partners.json', 'static/resources/logos')
    if result['errors']:
        return template('auth',
                       title="Partner Companies",
                       year=datetime.now().year,
                       companies=result['companies'],
                       form_data=result['form_data'],
                       errors=result['errors'])
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
                            error="Please fix the errors in the form.",
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
    return static_file(filename, root='static/resources/logos')