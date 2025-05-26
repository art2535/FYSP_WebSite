from bottle import route, view, request, redirect, response, template, static_file
from datetime import datetime
import traceback
from bottle import HTTPResponse  # Добавим этот импорт

from services.partner_service import get_partners, add_partners
from services.user_service import register_user, authenticate_user, logout_user
from services.new_products_service import load_news, save_news, validate_news_form, add_news, delete_news,find_images,enrich_news_items

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
        return template('partner',
                       title="Partner Companies",
                       year=datetime.now().year,
                       companies=result['companies'],
                       form_data=result['form_data'],
                       errors=result['errors'])
    redirect('/partners')

import traceback

@route('/new_products', method=['GET', 'POST'])
def new_products():
    images = find_images()

    if request.method == 'POST':
        delete_index = request.forms.get('delete_index')
        if delete_index is not None:
            try:
                index = int(delete_index)
                delete_news(index)
            except Exception as e:
                with open('error.log', 'a', encoding='utf-8') as log_file:
                    log_file.write(f"{datetime.now()} DELETE ERROR: {str(e)}\n")
                    traceback.print_exc(file=log_file)
            return HTTPResponse(status=303, location='/new_products')

        author = request.forms.get('author', '').strip()
        text = request.forms.get('text', '').strip()
        date = request.forms.get('date', '').strip()
        image = request.forms.get('image', '').strip()  # <-- добавлено

        try:
            errors = validate_news_form(author, text, date)
            if not errors:
                add_news(author, text, date, image if image else None)  # <-- добавлено
                return HTTPResponse(status=303, location='/new_products')
            else:
                return template('new_products.tpl',
                                new_products=enrich_news_items(load_news()),
                                error="Please fix the errors in the form.",
                                errors=errors,
                                author=author,
                                text=text,
                                date=date,
                                image=image,
                                images=images,
                                year=datetime.now().year)
        except HTTPResponse:
            raise
        except Exception as e:
            error_message = f"Exception occurred: {str(e)}"
            print(error_message)
            with open('error.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{datetime.now()}: {error_message}\n")
                traceback.print_exc(file=log_file)
            return template('new_products.tpl',
                            new_products=enrich_news_items(load_news()),
                            error="Internal error: что-то пошло не так.",
                            errors={},
                            author=author,
                            text=text,
                            date=date,
                            image=image,
                            images=images,
                            year=datetime.now().year)

    # GET запрос
    return template('new_products.tpl',
                    new_products = enrich_news_items(load_news()),
                    error=None,
                    errors={},
                    author='',
                    text='',
                    date='',
                    image='',
                    images=images,
                    year=datetime.now().year)


@route('/logos/<filename>')
def serve_logo(filename):
    return static_file(filename, root='static/resources/logos')