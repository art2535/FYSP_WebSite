import os
import json
from datetime import datetime
import re
import traceback  # Для логирования исключений

# Импорты из Bottle для работы с HTTP-ответами и шаблонами
from bottle import HTTPResponse, template

# Определение пути к файлу статей относительно текущего файла сервиса
ARTICLES_FILE = os.path.join(os.path.dirname(__file__), '..', 'static',
                             'resources', 'articles.json')


def load_articles():
    """Loads articles from the JSON file, sorted by date descending."""
    if os.path.exists(ARTICLES_FILE):  #
        try:
            with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)  #
                if not isinstance(data, list):
                    return []
                for article in data:
                    if 'link' not in article:  #
                        article['link'] = None  #
                return sorted(data, key=lambda x: x.get('date', ''),
                              reverse=True)  #
        except json.JSONDecodeError:  #
            return []
        except Exception:
            return []
    return []


def save_articles(articles_list):
    """Saves the list of articles to the JSON file."""
    try:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles_list, f, ensure_ascii=False, indent=2)  #
    except Exception as e:
        # В реальном приложении здесь должно быть более серьезное логирование
        print(f"Error saving articles: {e}")  #


def validate_article_form(title, author, text, date, link):
    """Validates the new article form fields, including the link."""
    errors = {}

    # Title validation
    title_stripped = title.strip()  #
    if not title_stripped:  #
        errors['title'] = "Поле 'Заголовок' не может быть пустым."
    elif len(title_stripped) <= 5:  #
        errors['title'] = "Поле 'Заголовок' должно содержать более 5 символов."
    elif len(title_stripped) > 50:  #
        errors['title'] = "Поле 'Заголовок' не должно превышать 50 символов."

    # Author validation
    author_stripped = author.strip()  #
    if not author_stripped:  #
        errors['author'] = "Поле 'Автор' не может быть пустым."
    elif not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", author_stripped):  #
        errors[
            'author'] = "Поле 'Автор' должно содержать только буквы и пробелы."
    elif not (2 <= len(author_stripped) <= 40):  #
        errors['author'] = "Поле 'Автор' должно содержать от 2 до 40 символов."

    # Text validation
    text_stripped = text.strip()  #
    if not text_stripped:  #
        errors['text'] = "Поле 'Текст' не может быть пустым."
    elif len(text_stripped) < 10:  #
        errors['text'] = "Поле 'Текст' должно содержать не менее 10 символов."

    # Date validation
    date_stripped = date.strip()  #
    if not date_stripped:  #
        errors['date'] = "Поле 'Дата' не может быть пустым."
    else:
        try:
            article_date = datetime.strptime(date_stripped,
                                             '%Y-%m-%d').date()  #
            if article_date > datetime.now().date():  #
                errors['date'] = "Дата не может быть в будущем."
        except ValueError:  #
            errors[
                'date'] = "Некорректный формат даты. Используйте ГГГГ-ММ-ДД."

    # Link validation
    if not link or not link.strip():  #
        errors['link'] = "Поле 'Ссылка' не может быть пустым."
    else:
        link_stripped = link.strip()  #
        if not (link_stripped.startswith(
                'http://') or link_stripped.startswith('https://')):  #
            errors[
                'link'] = "Ссылка должна начинаться с 'http://' или 'https://'."
        else:
            if link_stripped == 'http://' or link_stripped == 'https://':  #
                errors[
                    'link'] = "Ссылка должна содержать доменное имя после 'http://' или 'https://'."
            else:
                if link_stripped.startswith('http://'):  #
                    domain_part_with_path = link_stripped[7:]  #
                else:  # link_stripped.startswith('https://')
                    domain_part_with_path = link_stripped[8:]  #

                if not domain_part_with_path or domain_part_with_path.startswith(
                        '/'):  #
                    errors[
                        'link'] = "Требуется действительное доменное имя после 'http://' или 'https://'."
                else:
                    domain_name = domain_part_with_path.split('/', 1)[0]  #
                    if not domain_name:  #
                        errors[
                            'link'] = "Требуется действительное доменное имя."
                    elif ' ' in domain_name:  #
                        errors[
                            'link'] = "Имя домена в ссылке не может содержать пробелов."
                    else:
                        is_localhost = domain_name.lower() == "localhost"  #
                        is_ip_address = bool(re.match(
                            r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$",
                            domain_name))  #

                        if not is_localhost and not is_ip_address:
                            if '.' not in domain_name:  #
                                errors[
                                    'link'] = "Ссылка не содержит действительного доменного имени (например, example.com)."
                            else:
                                parts = domain_name.split('.')
                                if len(parts) < 2 or not parts[-1]:
                                    errors[
                                        'link'] = "Структура доменного имени в ссылке неверна (например, example.com)."
                                elif len(parts[-1]) < 2:
                                    errors[
                                        'link'] = "Домен верхнего уровня (например, '.com', '.org') должен содержать не менее 2 символов."

        if len(link_stripped) > 2048:  #
            if 'link' not in errors:  #
                errors[
                    'link'] = "Ссылка слишком длинная (максимум 2048 символов)."
            elif "слишком длинная" not in errors['link']:  #
                errors[
                    'link'] += " Также, ссылка слишком длинная (максимум 2048 символов)."  #
    return errors


def add_article(title, author, text, date, link):
    """Adds a new article to the list and saves it."""
    articles_list = load_articles()  #
    new_article = {
        'title': title.strip(),  #
        'author': author.strip(),  #
        'text': text.strip(),  #
        'date': date.strip(),  #
        'link': link.strip()  #
    }
    articles_list.insert(0, new_article)  #
    save_articles(articles_list)  #
    return new_article


def delete_article(index):  #
    """Deletes an article by its index. (Можно удалить, если не используется)"""
    articles_list = load_articles()  #
    if 0 <= index < len(articles_list):  #
        del articles_list[index]  #
        save_articles(articles_list)  #
        return True  #
    return False  #


# --- Новые функции-обработчики для маршрутов ---

def handle_articles_get_request():
    """
    Обрабатывает GET-запрос для страницы статей.
    Загружает статьи и отображает их с помощью шаблона.
    """
    current_articles = load_articles()
    # Убедитесь, что 'articles.tpl' доступен и правильно настроен
    return template('articles',  # Имя вашего файла шаблона
                    articles=current_articles,
                    errors={},
                    form_data={},  # Пустые данные формы для GET запроса
                    year=datetime.now().year,
                    title_page="Articles"  # Или "Статьи", если предпочитаете
                    )


def handle_articles_post_request(form_data_from_request):
    """
    Обрабатывает POST-запрос для добавления новой статьи.
    Извлекает данные из формы, валидирует их, добавляет статью или возвращает ошибки.
    """
    title = form_data_from_request.get('title', '').strip()
    author = form_data_from_request.get('author', '').strip()
    text = form_data_from_request.get('text', '').strip()
    date = form_data_from_request.get('date', '').strip()
    link = form_data_from_request.get('link', '').strip()

    form_data_to_template = {'title': title, 'author': author, 'text': text,
                             'date': date, 'link': link}
    errors = validate_article_form(title, author, text, date, link)

    if not errors:
        try:
            add_article(title, author, text, date, link)
            return HTTPResponse(status=303,
                                location='/articles')  # Редирект после успешного добавления
        except Exception as e:
            # Логирование ошибки
            error_log_message = f"{datetime.now()} ARTICLE ADD ERROR (from service): {str(e)}\n"
            with open('error.log', 'a', encoding='utf-8') as log_file:
                log_file.write(error_log_message)
                traceback.print_exc(file=log_file)

            current_articles = load_articles()
            return template('articles',
                            articles=current_articles,
                            errors={
                                'form': 'Произошла внутренняя ошибка при добавлении статьи. Пожалуйста, попробуйте еще раз.'},
                            form_data=form_data_to_template,
                            year=datetime.now().year,
                            title_page="Articles"  # Или "Статьи"
                            )
    else:  # Если есть ошибки валидации
        current_articles = load_articles()
        return template('articles',
                        articles=current_articles,
                        errors=errors,
                        form_data=form_data_to_template,
                        year=datetime.now().year,
                        title_page="Articles"  # Или "Статьи"
                        )