import json
from datetime import datetime

# Load products from JSON file
with open('static/resources/products.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)['products']

# Map product IDs to names for quick lookup
product_map = {str(product['id']): product['name'] for product in products_data}

# Initial reviews with product names added for existing product reviews
reviews_data = [
    {
        'avatar_url': '/static/Images/avatar1.jpg',
        'nickname': 'Denlelush',
        'category': 'product',
        'rating': 4,
        'text': 'I bought a figure of an anime creature, it seems to work, but it leaves visible fingerprints.',
        'date': '2025-05-14',
        'product_id': '1',
        'product_name': product_map['1']
    },
    {
        'avatar_url': '/static/Images/avatar2.jpg',
        'nickname': 'Kirill',
        'category': 'company',
        'rating': 5,
        'text': 'The company is great, I want to work here...',
        'date': '2025-05-10'
    },
    {
        'avatar_url': '/static/Images/avatar3.jpg',
        'nickname': 'Andrew',
        'category': 'product',
        'rating': 3,
        'text': 'They were supposed to get an iPhone 15 PRO MAX, but they were given an iPhone XR instead.',
        'date': '2025-05-08',
        'product_id': '2',
        'product_name': product_map['2']
    }
]

def add_review(nickname, category, rating, text, product_id=None):
    # Current date for the review
    date = datetime.now().strftime('%Y-%m-%d')

    # Create new review
    new_review = {
        'avatar_url': '/static/Images/avatar1.jpg',
        'nickname': nickname,
        'category': category,
        'rating': rating,
        'text': text,
        'date': date
    }

    # Add product info if category is product
    if category == 'product' and product_id in product_map:
        new_review['product_id'] = product_id
        new_review['product_name'] = product_map[product_id]

    reviews_data.append(new_review)

def get_reviews():
    return reviews_data

def get_products():
    return products_data
