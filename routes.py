from bottle import route, view, request, redirect, response, template, static_file
from datetime import datetime
import traceback
from bottle import HTTPResponse  # Добавим этот импорт

from services.partner_service import get_partners, add_partners
from services.reviews_service import add_review, get_form_data_from_request, get_products, get_reviews, validate_review
from services.user_service import register_user, authenticate_user, logout_user
from services.new_products_service import load_news, save_news, validate_news_form, add_news, delete_news,find_images,enrich_news_items
from services.article_service import load_articles, add_article, validate_article_form, delete_article


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
@view('articles') # Assuming your template will be named articles.tpl
def articles_page():
    form_data_to_template = {} # Для сохранения введенных данных при ошибке

    if request.method == 'POST':
        # Удаление статьи (старая логика остается, но кнопка будет другой)
        # Если вам не нужна логика удаления по индексу через форму, эту часть можно убрать
        delete_index_str = request.forms.get('delete_index')
        if delete_index_str is not None:
            try:
                index = int(delete_index_str)
                if delete_article(index):
                    return HTTPResponse(status=303, location='/articles')
                else:
                    print(f"Attempted to delete article at index {index}, but it was not found or failed.")
            except ValueError:
                print("Invalid delete index format.")
            except Exception as e:
                with open('error.log', 'a', encoding='utf-8') as log_file:
                    log_file.write(f"{datetime.now()} ARTICLE DELETE ERROR: {str(e)}\n")
                    traceback.print_exc(file=log_file)
            return HTTPResponse(status=303, location='/articles')

        # Добавление новой статьи
        title = request.forms.get('title', '').strip()
        author = request.forms.get('author', '').strip()
        text = request.forms.get('text', '').strip()
        date = request.forms.get('date', '').strip()
        link = request.forms.get('link', '').strip() # Получаем новую ссылку

        form_data_to_template = {'title': title, 'author': author, 'text': text, 'date': date, 'link': link}

        errors = validate_article_form(title, author, text, date, link) # Передаем ссылку на валидацию

        if not errors:
            try:
                add_article(title, author, text, date, link) # Передаем ссылку для добавления
                return HTTPResponse(status=303, location='/articles')
            except Exception as e:
                with open('error.log', 'a', encoding='utf-8') as log_file:
                    log_file.write(f"{datetime.now()} ARTICLE ADD ERROR: {str(e)}\n")
                    traceback.print_exc(file=log_file)
                current_articles = load_articles()
                return template('articles',
                    articles=current_articles,
                    errors={'form': 'An internal error occurred while adding the article. Please try again.'},
                    form_data=form_data_to_template, # Используем сохраненные данные
                    year=datetime.now().year,
                    title_page="Articles"
                )
        else: # Если есть ошибки валидации
            current_articles = load_articles()
            return template('articles',
                articles=current_articles,
                errors=errors,
                form_data=form_data_to_template, # Используем сохраненные данные
                year=datetime.now().year,
                title_page="Articles"
            )

    # GET request
    current_articles = load_articles()
    return template('articles',
        articles=current_articles,
        errors={},
        form_data=form_data_to_template if form_data_to_template else {}, # Передаем пустой словарь, если не было POST запроса с ошибками
        year=datetime.now().year,
        title_page="Articles"
    )


@route('/logos/<filename>')
def serve_logo(filename):
    return static_file(filename, root='static/resources/logos')