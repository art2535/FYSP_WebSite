import json
from datetime import datetime
import random
import re

REVIEWS_JSON_PATH = 'static/resources/reviews.json'

# Load products data from JSON file
with open('static/resources/products.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)['products']

# Create a mapping from product ID to product name for quick lookup
product_map = {str(product['id']): product['name'] for product in products_data}

# Load existing reviews from JSON file
with open(REVIEWS_JSON_PATH, 'r', encoding='utf-8') as f:
    raw_reviews = json.load(f)['reviews']

reviews_data = []
# Add product_name to product reviews based on product_id, defaulting to 'Unknown product'
for review in raw_reviews:
    if review.get('category') == 'product' and 'product_id' in review:
        pid = review['product_id']
        review['product_name'] = product_map.get(pid, 'Unknown product')
    reviews_data.append(review)


def save_reviews():
    """
    Save the current list of reviews back to the JSON file.
    Uses pretty printing with indentation for readability.
    """
    with open(REVIEWS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({'reviews': reviews_data}, f, ensure_ascii=False, indent=4)


def validate_review(nickname, category, rating, text, product_id):
    """
    Validate the inputs for a review submission.

    Parameters:
        nickname (str): The user's nickname.
        category (str): Category of the review ('company' or 'product').
        rating (str/int): Rating value as string or int.
        text (str): The text of the review.
        product_id (str or None): The ID of the product if category is 'product'.

    Returns:
        list: A list of error messages (empty if no errors).
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

        # Check for duplicate nicknames (case insensitive)
        existing_nicknames = {review['nickname'].lower() for review in reviews_data}
        if nickname.lower() in existing_nicknames:
            errors.append("This nickname is already taken. Please choose another.")

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

        # Ensure text is not only digits or special characters
        if re.fullmatch(r'[\d\W_]+', text, re.UNICODE):
            errors.append("Review text cannot consist only of digits or special characters.")

    # Validate product_id if category is 'product'
    if category == 'product':
        if not product_id or product_id not in product_map:
            errors.append("Please select a valid product.")

    return errors


def add_review(nickname, category, rating, text, product_id=None):
    """
    Add a new review if inputs are valid.

    Parameters:
        nickname (str): The user's nickname.
        category (str): Review category ('company' or 'product').
        rating (str/int): Rating value.
        text (str): Review text.
        product_id (str or None): Product ID if category is 'product'.

    Returns:
        tuple: (success (bool), errors (list or None))
            success is True if review was added successfully.
            errors is None if success, or a list of validation error messages.
    """
    errors = validate_review(nickname, category, rating, text, product_id)
    if errors:
        return False, errors

    # Current date in 'YYYY-MM-DD' format
    date = datetime.now().strftime('%Y-%m-%d')

    # Randomly assign avatar image URL
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

    # Append new review to in-memory data and save to file
    reviews_data.append(new_review)
    save_reviews()
    return True, None


def get_reviews(filter_category='all', sort_order=None):
    """
    Retrieve reviews with optional filtering by category and sorting by date.

    Parameters:
        filter_category (str): 'all', 'company', or 'product'. Default is 'all'.
        sort_order (str or None): 'new' for newest first, 'old' for oldest first, or None for no sorting.

    Returns:
        list: List of reviews matching the criteria.
    """
    # Filter by category if specified
    filtered_reviews = reviews_data
    if filter_category != 'all':
        filtered_reviews = [review for review in reviews_data if review['category'] == filter_category]

    # Sort by date if requested
    if sort_order:
        filtered_reviews = sorted(
            filtered_reviews,
            key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'),
            reverse=(sort_order == 'new')
        )

    return filtered_reviews


def get_products():
    """
    Retrieve the list of available products.

    Returns:
        list: List of product dictionaries loaded from JSON.
    """
    return products_data


def get_form_data_from_request(request):
    """
    Extract form data from a POST request for review submission.

    Parameters:
        request: The incoming request object with form data.

    Returns:
        dict: Dictionary with keys 'nickname', 'category', 'rating', 'text', 'product_id'
              populated with the submitted form data or default empty values.
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
