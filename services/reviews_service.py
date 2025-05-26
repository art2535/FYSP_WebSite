import json
from datetime import datetime
import random
import re

REVIEWS_JSON_PATH = 'static/resources/reviews.json'

with open('static/resources/products.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)['products']

product_map = {str(product['id']): product['name'] for product in products_data}

with open(REVIEWS_JSON_PATH, 'r', encoding='utf-8') as f:
    raw_reviews = json.load(f)['reviews']

reviews_data = []
for review in raw_reviews:
    if review.get('category') == 'product' and 'product_id' in review:
        pid = review['product_id']
        review['product_name'] = product_map.get(pid, 'Unknown product')
    reviews_data.append(review)

def save_reviews():
    with open(REVIEWS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({'reviews': reviews_data}, f, ensure_ascii=False, indent=4)

def validate_review(nickname, category, rating, text, product_id):
    errors = []

    if not nickname:
        errors.append("Nickname is required.")
    else:
        if len(nickname) < 2:
            errors.append("Nickname must be at least 2 characters long.")
        if len(nickname) > 20:
            errors.append("Nickname cannot be longer than 20 characters.")
        if not re.search('[a-zA-Z]', nickname):
            errors.append("Nickname must contain at least one letter.")
        if not re.fullmatch(r'[a-zA-Z0-9]+', nickname):
            errors.append("Nickname can only contain letters and numbers, no special characters.")
        existing_nicknames = {review['nickname'].lower() for review in reviews_data}
        if nickname.lower() in existing_nicknames:
            errors.append("This nickname is already taken. Please choose another.")

    try:
        rating_val = int(rating)
        if rating_val < 1 or rating_val > 5:
            errors.append("Rating must be a number between 1 and 5.")
    except (ValueError, TypeError):
        errors.append("Rating must be a valid number.")

    if not text:
        errors.append("Review text is required.")
    else:
        if len(text) > 150:
            errors.append("Review text cannot exceed 150 characters.")

        letter_count = len(re.findall(r'[a-zA-Z]', text))
        if letter_count < 3:
            errors.append("Review text must contain at least 3 letters.")

        if re.fullmatch(r'[\d\W_]+', text, re.UNICODE):
            errors.append("Review text cannot consist only of digits or special characters.")

    if category == 'product':
        if not product_id or product_id not in product_map:
            errors.append("Please select a valid product.")

    return errors

def add_review(nickname, category, rating, text, product_id=None):
    errors = validate_review(nickname, category, rating, text, product_id)
    if errors:
        return False, errors

    date = datetime.now().strftime('%Y-%m-%d')

    avatar_num = random.randint(1, 4)
    avatar_url = f'/static/resources/avatars/avatar{avatar_num}.jpg'

    new_review = {
        'avatar_url': avatar_url,
        'nickname': nickname,
        'category': category,
        'rating': int(rating),
        'text': text,
        'date': date
    }

    if category == 'product':
        new_review['product_id'] = product_id
        new_review['product_name'] = product_map[product_id]

    reviews_data.append(new_review)
    save_reviews()
    return True, None

def get_reviews(filter_category='all', sort_order=None):
    # Filter reviews by category
    filtered_reviews = reviews_data
    if filter_category != 'all':
        filtered_reviews = [review for review in reviews_data if review['category'] == filter_category]

    # Sort reviews by date
    if sort_order:
        filtered_reviews = sorted(
            filtered_reviews,
            key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'),
            reverse=(sort_order == 'new')
        )

    return filtered_reviews

def get_products():
    return products_data


def get_form_data_from_request(request):
    form_data = {
        'nickname': '',
        'category': 'company',
        'rating': '',
        'text': '',
        'product_id': ''
    }

    if request.method == 'POST':
        form_data.update({
            'nickname': request.forms.get('nickname'),
            'category': request.forms.get('category'),
            'rating': request.forms.get('rating'),
            'text': request.forms.get('text'),
            'product_id': request.forms.get('product_id'),
        })

    return form_data
