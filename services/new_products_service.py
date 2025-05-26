import os
import json
from datetime import datetime

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

    if not author:
        errors['author'] = "The 'Brand / Name' field is required."
    if not text:
        errors['text'] = "The 'Description' field is required."
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
