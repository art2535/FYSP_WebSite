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
                    print("⚠️ Ожидался список, но получен другой тип.")
                    return []
                return sorted(data, key=lambda x: x.get('date', ''), reverse=True)
        except json.JSONDecodeError as e:
            print(f"⚠️ Ошибка чтения JSON: {e}")
            return []
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

def add_news(author, text, date):
    news_list = load_news()
    news_list.insert(0, {'author': author, 'text': text, 'date': date})
    save_news(news_list)

def delete_news(index):
    news_list = load_news()
    if 0 <= index < len(news_list):
        del news_list[index]
        save_news(news_list)
