import json
from datetime import datetime
import random
import re

# Path to the reviews JSON file
REVIEWS_JSON_PATH = 'static/resources/reviews.json'

# Load product data from products.json
with open('static/resources/products.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)['products']

# Create a mapping from product ID to product name
product_map = {str(product['id']): product['name'] for product in products_data}

# Load raw reviews from JSON
with open(REVIEWS_JSON_PATH, 'r', encoding='utf-8') as f:
    raw_reviews = json.load(f).get('reviews', {})

# Initialize reviews_data: dict with nickname as key, list of reviews as value
reviews_data = {}
for nickname, user_reviews in raw_reviews.items():
    reviews_data[nickname] = []
    for review in user_reviews:
        if review.get('category') == 'product' and 'product_id' in review:
            pid = review['product_id']
            review['product_name'] = product_map.get(pid, 'Unknown product')
        reviews_data[nickname].append(review)


def save_reviews():
    """
    Save the current state of reviews_data to the JSON file.
    """
    with open(REVIEWS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({'reviews': reviews_data}, f, ensure_ascii=False, indent=4)


def validate_review(nickname, category, rating, text, product_id):
    """
    Validate review form data before submission.

    Args:
        nickname (str): User's nickname.
        category (str): Review category ('company' or 'product').
        rating (str or int): Review rating (1 to 5).
        text (str): Review text.
        product_id (str): Product ID (required for product reviews).

    Returns:
        list[str]: List of error messages, empty if valid.
    """
    errors = []

    # Validate nickname
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

    # Validate rating
    try:
        rating_val = int(rating)
        if rating_val < 1 or rating_val > 5:
            errors.append("Rating must be a number between 1 and 5.")
    except (ValueError, TypeError):
        errors.append("Rating must be a valid number.")

    # Validate review text
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

    # Validate product_id if category is product
    if category == 'product':
        if not product_id or product_id not in product_map:
            errors.append("Please select a valid product.")

    existing_reviews = reviews_data.get(nickname, [])
    for review in existing_reviews:
        if category == 'company' and review['category'] == 'company':
            errors.append("You have already left a review about the company.")
            break
        if category == 'product' and review['category'] == 'product' and review.get('product_id') == product_id:
            product_name = product_map.get(product_id, "this product")
            errors.append(f"Have you already left a review about the product: {product_name}.")
            break

    return errors


def add_review(nickname, category, rating, text, product_id=None):
    """
    Add a new review to reviews_data after validating the input.

    Args:
        nickname (str): User's nickname.
        category (str): Review category ('company' or 'product').
        rating (str or int): Review rating (1 to 5).
        text (str): Review content.
        product_id (str, optional): Product ID for product reviews.

    Returns:
        tuple: (success (bool), errors (list or None))
    """
    errors = validate_review(nickname, category, rating, text, product_id)
    if errors:
        return False, errors

    date = datetime.now().strftime('%Y-%m-%d')
    avatar_url = f'/static/resources/avatars/avatar{random.randint(1, 4)}.jpg'

    new_review = {
        'avatar_url': avatar_url,
        'category': category,
        'rating': int(rating),
        'text': text,
        'date': date
    }

    if category == 'product':
        new_review['product_id'] = product_id
        new_review['product_name'] = product_map[product_id]

    reviews_data.setdefault(nickname, []).append(new_review)

    save_reviews()
    return True, None


def get_reviews(filter_category='all', sort_order=None):
    """
    Retrieve reviews from the dataset with optional filtering and sorting.

    Args:
        filter_category (str): 'company', 'product', or 'all' (default).
        sort_order (str): 'new' for newest first, 'old' for oldest first.

    Returns:
        list[dict]: List of reviews.
    """
    all_reviews = []
    for nickname, user_reviews in reviews_data.items():
        for review in user_reviews:
            full_review = review.copy()
            full_review['nickname'] = nickname
            all_reviews.append(full_review)

    if filter_category != 'all':
        all_reviews = [r for r in all_reviews if r['category'] == filter_category]

    if sort_order:
        all_reviews = sorted(
            all_reviews,
            key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'),
            reverse=(sort_order == 'new')
        )

    return all_reviews


def get_products():
    """
    Retrieve the list of available products.

    Returns:
        list[dict]: List of products with 'id' and 'name'.
    """
    return products_data


def get_form_data_from_request(request):
    """
    Extract and normalize form data from a Bottle request.

    Args:
        request (bottle.Request): Incoming request object.

    Returns:
        dict: Normalized form data with default values if missing.
    """
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