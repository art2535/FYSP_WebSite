import os
import json
from datetime import datetime
import re
import traceback

from bottle import HTTPResponse, template

# Получаем путь к файлу, где будут храниться статьи.
# Файл находится в подкаталоге "static/resources" рядом с текущим модулем.
ARTICLES_FILE = os.path.join(os.path.dirname(__file__), '..', 'static',
                             'resources', 'articles.json')


def load_articles():
    """
    Загружает статьи из JSON-файла и возвращает их как список.
    Если файл отсутствует или формат неверный — возвращается пустой список.
    """
    if os.path.exists(ARTICLES_FILE):
        try:
            # Открываем файл и читаем его содержимое
            with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Проверка, что данные — список (ожидаемый формат)
                if not isinstance(data, list):
                    return []

                # Убедимся, что в каждой статье есть ключ 'link'
                for article in data:
                    if 'link' not in article:
                        article['link'] = None

                # Сортировка по дате (новые статьи сверху)
                return sorted(data, key=lambda x: x.get('date', ''),
                              reverse=True)

        except json.JSONDecodeError:
            # Ошибка чтения JSON — возвращаем пустой список
            return []
        except Exception:
            # Любая другая ошибка — тоже возвращаем пустой список
            return []
    return []


def save_articles(articles_list):
    """
    Сохраняет список статей в JSON-файл.
    Используется при добавлении или удалении статьи.
    """
    try:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # При ошибке выводим сообщение (можно заменить на лог в проде)
        print(f"Error saving articles: {e}")


def validate_article_form(title, author, text, date, link):
    """
    Проверяет корректность введённых пользователем данных.
    Возвращает словарь с ошибками (если есть), где ключ — имя поля, а значение — текст ошибки.
    """
    errors = {}

    # Проверка заголовка статьи
    title_stripped = title.strip()
    if not title_stripped:
        errors['title'] = "The 'Title' field cannot be empty."
    elif len(title_stripped) <= 5:
        errors['title'] = "The 'Title' must be longer than 5 characters."
    elif len(title_stripped) > 50:
        errors['title'] = "The 'Title' must not exceed 50 characters."

    # Проверка имени автора
    author_stripped = author.strip()
    if not author_stripped:
        errors['author'] = "The 'Author' field cannot be empty."
    elif not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", author_stripped):
        errors[
            'author'] = "The 'Author' field must contain only letters and spaces."
    elif not (2 <= len(author_stripped) <= 40):
        errors['author'] = "The 'Author' must be between 2 and 40 characters."

    # Проверка текста статьи
    text_stripped = text.strip()
    if not text_stripped:
        errors['text'] = "The 'Text' field cannot be empty."
    elif len(text_stripped) < 10:
        errors['text'] = "The 'Text' must be at least 10 characters long."

    # Проверка даты публикации
    date_stripped = date.strip()
    if not date_stripped:
        errors['date'] = "The 'Date' field cannot be empty."
    else:
        try:
            article_date = datetime.strptime(date_stripped, '%Y-%m-%d').date()
            if article_date > datetime.now().date():
                errors['date'] = "The date cannot be in the future."
        except ValueError:
            errors['date'] = "Invalid date format. Use YYYY-MM-DD."

    # Проверка ссылки на источник
    if not link or not link.strip():
        errors['link'] = "The 'Link' field cannot be empty."
    else:
        link_stripped = link.strip()
        if not (link_stripped.startswith(
                'http://') or link_stripped.startswith('https://')):
            errors[
                'link'] = "The link must start with 'http://' or 'https://'."
        else:
            if link_stripped in ('http://', 'https://'):
                errors[
                    'link'] = "The link must contain a domain name after the scheme."
            else:
                # Отделяем доменное имя от пути
                domain_part_with_path = link_stripped[
                                        7:] if link_stripped.startswith(
                    'http://') else link_stripped[8:]

                if not domain_part_with_path or domain_part_with_path.startswith(
                        '/'):
                    errors[
                        'link'] = "A valid domain name is required after 'http://' or 'https://'."
                else:
                    domain_name = domain_part_with_path.split('/', 1)[0]
                    if not domain_name:
                        errors['link'] = "The domain name cannot be empty."
                    elif ' ' in domain_name:
                        errors[
                            'link'] = "The domain name cannot contain spaces."
                    else:
                        # Поддержка IP-адресов и localhost
                        # Для localhost, проверяем основную часть доменного имени (до ':')
                        domain_name_for_localhost_check = \
                        domain_name.split(':')[0]
                        is_localhost = domain_name_for_localhost_check.lower() == "localhost"

                        # Regex для IP может включать порт
                        is_ip_address = bool(
                            re.match(r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$",
                                     domain_name))

                        if not is_localhost and not is_ip_address:
                            # Стандартная валидация доменного имени
                            if '.' not in domain_name:
                                errors[
                                    'link'] = "The link must contain a valid domain name (e.g., example.com)."
                            else:
                                parts = domain_name.split('.')
                                # Проверяем на пустые части (например, ".com" -> ['', 'com'] или "example." -> ['example', ''])
                                # или если частей меньше двух.
                                if len(parts) < 2 or not parts[0] or not parts[
                                    -1]:
                                    errors[
                                        'link'] = "Invalid domain structure (e.g., example.com)."
                                elif len(parts[-1]) < 2:  # Длина TLD
                                    errors[
                                        'link'] = "Top-level domain must be at least 2 characters."

        # Проверка длины ссылки
        if len(link_stripped) > 2048:
            if 'link' not in errors:  # Если ошибки по ссылке еще не было
                errors[
                    'link'] = "The link is too long (maximum 2048 characters)."
            elif "too long" not in errors[
                'link']:  # Если была, но не про длину
                errors[
                    'link'] += " Also, the link is too long (maximum 2048 characters)."

    return errors


def add_article(title, author, text, date, link):
    """
    Добавляет новую статью в начало списка и сохраняет обновлённый файл.
    """
    articles_list = load_articles()
    new_article = {
        'title': title.strip(),
        'author': author.strip(),
        'text': text.strip(),
        'date': date.strip(),
        'link': link.strip()
    }
    # Вставляем статью в начало (чтобы новые были первыми)
    articles_list.insert(0, new_article)
    save_articles(articles_list)
    return new_article


def delete_article(index):
    """
    Удаляет статью по индексу из списка.
    Если индекс валиден — сохраняет изменения и возвращает True.
    """
    articles_list = load_articles()
    if 0 <= index < len(articles_list):
        del articles_list[index]
        save_articles(articles_list)
        return True
    return False


def handle_articles_get_request():
    """
    Обрабатывает GET-запрос к /articles.
    Загружает статьи и рендерит шаблон с ними.
    """
    current_articles = load_articles()
    return template('articles',
                    articles=current_articles,
                    errors={},
                    form_data={},
                    year=datetime.now().year,
                    title_page="Articles")


def handle_articles_post_request(form_data_from_request):
    """
    Обрабатывает POST-запрос с формы добавления статьи.
    Выполняет валидацию, добавляет статью или возвращает ошибки.
    """
    # Получение данных из формы и их очистка от пробелов
    title = form_data_from_request.get('title', '').strip()
    author = form_data_from_request.get('author', '').strip()
    text = form_data_from_request.get('text', '').strip()
    date = form_data_from_request.get('date', '').strip()
    link = form_data_from_request.get('link', '').strip()

    # Данные для повторного отображения в форме
    form_data_to_template = {
        'title': title,
        'author': author,
        'text': text,
        'date': date,
        'link': link
    }

    # Выполнение валидации
    errors = validate_article_form(title, author, text, date, link)

    if not errors:
        try:
            # Если ошибок нет — добавляем статью и редиректим
            add_article(title, author, text, date, link)
            return HTTPResponse(status=303, location='/articles')
        except Exception as e:
            # Логирование внутренней ошибки
            error_log_message = f"{datetime.now()} ARTICLE ADD ERROR (from service): {str(e)}\n"
            with open('error.log', 'a', encoding='utf-8') as log_file:
                log_file.write(error_log_message)
                traceback.print_exc(file=log_file)

            # Показываем ошибку пользователю
            current_articles = load_articles()
            return template('articles',
                            articles=current_articles,
                            errors={
                                'form': 'Internal error occurred while adding the article. Please try again.'},
                            form_data=form_data_to_template,
                            year=datetime.now().year,
                            title_page="Articles")
    else:
        # Если есть ошибки валидации — возвращаем форму с ошибками
        current_articles = load_articles()
        return template('articles',
                        articles=current_articles,
                        errors=errors,
                        form_data=form_data_to_template,
                        year=datetime.now().year,
                        title_page="Articles")