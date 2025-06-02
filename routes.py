from bottle import route, view, request, redirect, response, template, static_file
from datetime import datetime
import traceback
from bottle import HTTPResponse  # Добавим этот импорт

from services.partner_service import get_partners, add_partners
from services.reviews_service import add_review, get_form_data_from_request, get_products, get_reviews, validate_review
from services.user_service import register_user, authenticate_user, logout_user
from services.new_products_service import load_news, save_news, validate_news_form, add_news, delete_news,find_images,enrich_news_items
from services.article_service import handle_articles_get_request, handle_articles_post_request


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

@route('/reviews', method=['GET', 'POST'])
@view('reviews')
def reviews():
    errors = []
    form_data = get_form_data_from_request(request)

    if request.method == 'POST':
        errors = validate_review(
            form_data['nickname'],
            form_data['category'],
            form_data['rating'],
            form_data['text'],
            form_data['product_id']
        )

        if not errors:
            add_review(
                form_data['nickname'],
                form_data['category'],
                form_data['rating'],
                form_data['text'],
                form_data['product_id']
            )
            redirect('/reviews')

    filter_category = request.query.get('filter_category', 'all')
    sort_order = request.query.get('sort_order', '')
    if not sort_order:
        sort_order = 'new'

    return dict(
        title='Reviews',
        reviews=get_reviews(filter_category, sort_order),
        products=get_products(),
        year=datetime.now().year,
        errors=errors,
        form_data=form_data,
        filter_category=filter_category,
        sort_order=sort_order
    )


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

@route('/new_products', method=['GET', 'POST'])
def new_products():
    try:
        if request.method == 'POST':
            from services.new_products_service import process_news_form_submission
            return process_news_form_submission(request)

        # GET запрос
        from services.new_products_service import render_news_page
        return render_news_page()

    except HTTPResponse as http_resp:
        raise http_resp
    except Exception as e:
        from services.new_products_service import log_and_render_error
        return log_and_render_error(e)

@route('/articles', method=['GET', 'POST'])
def articles_page():
    if request.method == 'POST':
        return handle_articles_post_request(request.forms)
    else:
        return handle_articles_get_request()


@route('/logos/<filename>')
def serve_logo(filename):
    return static_file(filename, root='static/resources/logos')