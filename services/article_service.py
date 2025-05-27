import os
import json
from datetime import datetime

ARTICLES_FILE = 'static/resources/articles.json'

def load_articles():
    """Loads articles from the JSON file, sorted by date descending."""
    if os.path.exists(ARTICLES_FILE):
        try:
            with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                # Sort articles by date, newest first
                return sorted(data, key=lambda x: x.get('date', ''), reverse=True)
        except json.JSONDecodeError:
            return []  # Return empty list if JSON is malformed
        except Exception:
            # Catch any other unexpected errors during file reading or sorting
            return []
    return []

def save_articles(articles_list):
    """Saves the list of articles to the JSON file."""
    try:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # Log error or raise a custom exception if needed
        print(f"Error saving articles: {e}")


def validate_article_form(title, author, text, date):
    """Validates the new article form fields."""
    errors = {}
    if not title.strip():
        errors['title'] = "The 'Title' field is required."
    if not author.strip():
        errors['author'] = "The 'Author' field is required."
    if not text.strip():
        errors['text'] = "The 'Text' field is required."
    if not date.strip():
        errors['date'] = "The 'Date' field is required."
    else:
        try:
            article_date = datetime.strptime(date, '%Y-%m-%d').date()
            if article_date > datetime.now().date():
                errors['date'] = "The date cannot be in the future."
        except ValueError:
            errors['date'] = "Invalid date format. Use YYYY-MM-DD."
    return errors

def add_article(title, author, text, date):
    """Adds a new article to the list and saves it."""
    articles_list = load_articles()
    new_article = {
        'title': title.strip(),
        'author': author.strip(),
        'text': text.strip(),
        'date': date.strip()
    }
    # Add to the beginning to show newest first, consistent with load_articles sort
    articles_list.insert(0, new_article)
    save_articles(articles_list)
    return new_article

def delete_article(index):
    """Deletes an article by its index."""
    articles_list = load_articles() # Load fresh list before deleting
    if 0 <= index < len(articles_list):
        del articles_list[index]
        save_articles(articles_list)
        return True
    return False