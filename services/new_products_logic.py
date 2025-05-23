import os
import json
from datetime import datetime

NEWS_FILE = 'static/resources/news.json'

def load_news():
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            return sorted(json.load(f), key=lambda x: x['date'], reverse=True)
    return []

def save_news(news_list):
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

def validate_news_form(author, text, date):
    errors = {}

    if not author:
        errors['author'] = "Поле 'Имя / Название' обязательно."
    if not text:
        errors['text'] = "Поле 'Описание' обязательно."
    if not date:
        errors['date'] = "Поле 'Дата' обязательно."
    else:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            errors['date'] = "Неверный формат даты. Используйте ГГГГ-ММ-ДД."

    return errors
