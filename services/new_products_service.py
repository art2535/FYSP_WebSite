import os
import json
from datetime import datetime
import traceback
from bottle import template, HTTPResponse

NEWS_FILE = 'static/resources/news.json'

# Загружает список новостей из JSON-файла.
# Возвращает список новостей, отсортированный по дате (по убыванию).
def load_news():
    if os.path.exists(NEWS_FILE):  # Проверяем, существует ли файл
        try:
            with open(NEWS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Загружаем данные из JSON
                if not isinstance(data, list):  # Убеждаемся, что данные — это список
                    print("⚠️ Expected a list but got another type.")
                    return []
                # Сортируем список по дате, по убыванию
                return sorted(data, key=lambda x: x.get('date', ''), reverse=True)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON read error: {e}")
            return []
    return []

# Сохраняет список новостей в JSON-файл.
# Параметры:
#   news_list — список новостей для сохранения.
def save_news(news_list):
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        # Сохраняем с отступами и без экранирования Unicode
        json.dump(news_list, f, ensure_ascii=False, indent=2)

# Проверяет валидность полей формы добавления новости.
# Параметры:
#   author — строка, название бренда/автора.
#   text — строка, описание.
#   date — строка в формате 'YYYY-MM-DD'.
# Возвращает словарь с ошибками (если есть).
def validate_news_form(author, text, date):
    errors = {}

    # Вложенная функция: поле считается невалидным, если оно пустое, короткое или состоит только из цифр
    def is_invalid_field(value):
        return (
            not value or
            len(value.strip()) < 5 or
            value.strip().isdigit()
        )

    # Проверка поля автора
    if is_invalid_field(author):
        if not author.strip():
            errors['author'] = "The 'Brand / Name' field is required."
        elif len(author.strip()) < 5:
            errors['author'] = "Brand / Name must be at least 5 characters."
        elif author.strip().isdigit():
            errors['author'] = "Brand / Name cannot be only numbers."
        elif len(author.strip()) > 100:
            errors['author'] = "Brand / Name must be less than 100 characters.."

    # Проверка поля описания
    if is_invalid_field(text):
        if not text.strip():
            errors['text'] = "The 'Description' field is required."
        elif len(text.strip()) < 5:
            errors['text'] = "Description must be at least 5 characters."
        elif text.strip().isdigit():
            errors['text'] = "Description cannot be only numbers."
    elif len(text.strip()) > 200:
        errors['text'] = "Description must not exceed 200 characters."

    # Проверка поля даты
    if not date:
        errors['date'] = "The 'Date' field is required."
    else:
        try:
            # Преобразуем строку в дату
            input_date = datetime.strptime(date, '%Y-%m-%d').date()
            today = datetime.now().date()
            one_year_ago = today.replace(year=today.year - 1)
            one_year_future = today.replace(year=today.year + 1)

            # Проверяем, что дата в пределах одного года от текущей
            if input_date < one_year_ago or input_date > one_year_future:
                errors['date'] = "Date must be within one year from today."
        except ValueError:
            errors['date'] = "Invalid date format. Use YYYY-MM-DD."

    return errors

# Добавляет новость в список и сохраняет её в файл.
# Параметры:
#   author — название бренда.
#   text — описание.
#   date — дата публикации.
#   image — (опционально) путь к изображению.
def add_news(author, text, date, image=None):
    news_list = load_news()  # Загружаем существующие новости
    item = {'author': author, 'text': text, 'date': date}  # Формируем новую новость
    if image:
        item['image'] = image  # Добавляем изображение, если есть
    news_list.insert(0, item)  # Вставляем новость в начало списка
    save_news(news_list)  # Сохраняем

# Удаляет новость по индексу из списка.
# Параметры:
#   index — индекс новости в списке.
def delete_news(index):
    news_list = load_news()
    if 0 <= index < len(news_list):  # Убедимся, что индекс в допустимом диапазоне
        del news_list[index]
        save_news(news_list)

# Находит все изображения в указанной директории и её подпапках.
# Параметры:
#   root_dir — корневая папка для поиска (по умолчанию 'static/resources').
# Возвращает отсортированный список относительных путей к изображениям.
def find_images(root_dir='static/resources'):
    supported_ext = ('.png', '.jpeg', '.jpg')
    image_files = []
    for dirpath, _, filenames in os.walk(root_dir):  # Рекурсивно обходим директории
        for file in filenames:
            if file.lower().endswith(supported_ext):
                relative_path = os.path.relpath(os.path.join(dirpath, file), 'static/resources')
                # Преобразуем путь к виду с прямыми слэшами для кроссплатформенности
                image_files.append(relative_path.replace("\\", "/"))
    return sorted(image_files)

# Добавляет к каждой новости информацию о том, можно ли сделать предзаказ.
# Параметры:
#   news_items — список новостей.
# Возвращает обновлённый список с полями is_future и order_label.
def enrich_news_items(news_items):
    today = datetime.now().date()
    for item in news_items:
        item_date = datetime.strptime(item['date'], "%Y-%m-%d").date()
        item['is_future'] = item_date > today  # Признак, что дата в будущем
        item['order_label'] = "Pre-order" if item['is_future'] else "Order"
    return news_items

# Обрабатывает отправку формы: добавление или удаление новости.
# Параметры:
#   request — объект запроса Bottle.
# Возвращает перенаправление или шаблон с ошибками.
def process_news_form_submission(request):
    images = find_images()

    delete_index = request.forms.get('delete_index')
    if delete_index is not None:
        try:
            delete_news(int(delete_index))  # Удаление по индексу
        except Exception as e:
            log_exception(e, context="DELETE ERROR")
        # Перенаправляем после удаления
        return HTTPResponse(status=303, location='/new_products')

    # Получаем данные из формы
    author = request.forms.get('author', '').strip()
    text = request.forms.get('text', '').strip()
    date = request.forms.get('date', '').strip()
    image = request.forms.get('image', '').strip()

    errors = validate_news_form(author, text, date)
    if not errors:
        add_news(author, text, date, image if image else None)
        return HTTPResponse(status=303, location='/new_products')

    # Если ошибки есть, возвращаем шаблон с ошибками
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

# Рендерит страницу с формой и списком новостей без ошибок.
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

# Логирует исключение и возвращает страницу с сообщением об ошибке.
# Параметры:
#   exception — объект исключения.
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

# Записывает исключение в лог-файл с текущим временем и стеком вызовов.
# Параметры:
#   e — исключение.
#   context — строка-контекст для логирования.
def log_exception(e, context="ERROR"):
    with open('error.log', 'a', encoding='utf-8') as log_file:
        log_file.write(f"{datetime.now()} {context}: {str(e)}\n")  # Запись ошибки
        traceback.print_exc(file=log_file)  # Запись трассировки стека
