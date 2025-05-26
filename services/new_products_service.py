import os
import json
from datetime import datetime
import traceback
from bottle import template, HTTPResponse

NEWS_FILE = 'static/resources/news.json'

def load_news():
    if os.path.exists(NEWS_FILE):
        try:
            with open(NEWS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    print("⚠️ Expected a list but got another type.")
                    return []
                return sorted(data, key=lambda x: x.get('date', ''), reverse=True)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON read error: {e}")
            return []
    return []

def save_news(news_list):
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

def validate_news_form(author, text, date):
    errors = {}

    def is_invalid_field(value):
        return (
            not value or
            len(value.strip()) < 5 or
            value.strip().isdigit()
        )

    if is_invalid_field(author):
        if not author.strip():
            errors['author'] = "The 'Brand / Name' field is required."
        elif len(author.strip()) < 5:
            errors['author'] = "Brand / Name must be at least 5 characters."
        elif author.strip().isdigit():
            errors['author'] = "Brand / Name cannot be only numbers."
        elif len(author.strip()) > 100:
            errors['author'] = "Brand / Name must be less than 100 characters.."

    if is_invalid_field(text):
        if not text.strip():
            errors['text'] = "The 'Description' field is required."
        elif len(text.strip()) < 5:
            errors['text'] = "Description must be at least 5 characters."
        elif text.strip().isdigit():
            errors['text'] = "Description cannot be only numbers."
    elif len(text.strip()) > 200:
        errors['text'] = "Description must not exceed 200 characters."

    if not date:
        errors['date'] = "The 'Date' field is required."
    else:
        try:
            input_date = datetime.strptime(date, '%Y-%m-%d').date()
            today = datetime.now().date()
            one_year_ago = today.replace(year=today.year - 1)
            one_year_future = today.replace(year=today.year + 1)

            if input_date < one_year_ago or input_date > one_year_future:
                errors['date'] = "Date must be within one year from today."
        except ValueError:
            errors['date'] = "Invalid date format. Use YYYY-MM-DD."

    return errors


def add_news(author, text, date, image=None):
    news_list = load_news()
    item = {'author': author, 'text': text, 'date': date}
    if image:
        item['image'] = image
    news_list.insert(0, item)
    save_news(news_list)

def delete_news(index):
    news_list = load_news()
    if 0 <= index < len(news_list):
        del news_list[index]
        save_news(news_list)

def find_images(root_dir='static/resources'):
    supported_ext = ('.png', '.jpeg', '.jpg')
    image_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(supported_ext):
                relative_path = os.path.relpath(os.path.join(dirpath, file), 'static/resources')
                image_files.append(relative_path.replace("\\", "/"))  # for Windows compatibility
    return sorted(image_files)

def enrich_news_items(news_items):
    today = datetime.now().date()
    for item in news_items:
        item_date = datetime.strptime(item['date'], "%Y-%m-%d").date()
        item['is_future'] = item_date > today
        item['order_label'] = "Pre-order" if item['is_future'] else "Order"
    return news_items

def process_news_form_submission(request):
    images = find_images()

    delete_index = request.forms.get('delete_index')
    if delete_index is not None:
        try:
            delete_news(int(delete_index))
        except Exception as e:
            log_exception(e, context="DELETE ERROR")
        return HTTPResponse(status=303, location='/new_products')

    author = request.forms.get('author', '').strip()
    text = request.forms.get('text', '').strip()
    date = request.forms.get('date', '').strip()
    image = request.forms.get('image', '').strip()

    errors = validate_news_form(author, text, date)
    if not errors:
        add_news(author, text, date, image if image else None)
        return HTTPResponse(status=303, location='/new_products')

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


def render_news_page():
    return template('new_products.tpl',
                    new_products=enrich_news_items(load_news()),
                    error=None,
                    errors={},
                    author='',
                    text='',
                    date='',
                    image='',
                    images=find_images(),
                    year=datetime.now().year)


def log_and_render_error(exception):
    log_exception(exception, context="GENERAL ERROR")
    return template('new_products.tpl',
                    new_products=enrich_news_items(load_news()),
                    error="Internal error: что-то пошло не так.",
                    errors={},
                    author='',
                    text='',
                    date='',
                    image='',
                    images=find_images(),
                    year=datetime.now().year)


def log_exception(e, context="ERROR"):
    with open('error.log', 'a', encoding='utf-8') as log_file:
        log_file.write(f"{datetime.now()} {context}: {str(e)}\n")
        traceback.print_exc(file=log_file)
