import os
import json
from datetime import datetime
import re

ARTICLES_FILE = 'static/resources/articles.json'

def load_articles():
    """Loads articles from the JSON file, sorted by date descending."""
    if os.path.exists(ARTICLES_FILE):
        try:
            with open(ARTICLES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                for article in data:
                    if 'link' not in article:
                        article['link'] = None
                return sorted(data, key=lambda x: x.get('date', ''), reverse=True)
        except json.JSONDecodeError:
            return []
        except Exception:
            return []
    return []

def save_articles(articles_list):
    """Saves the list of articles to the JSON file."""
    try:
        with open(ARTICLES_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving articles: {e}")


def validate_article_form(title, author, text, date, link):
    """Validates the new article form fields, including the link."""
    errors = {}

    # Title validation
    if not title or not title.strip():
        errors['title'] = "The 'Title' field cannot be empty."
    elif len(title.strip()) <= 5:
        errors['title'] = "The 'Title' field must be longer than 5 characters."
    elif len(title.strip()) > 50:
        errors['title'] = "The 'Title' field cannot exceed 50 characters."

    # Author validation
    if not author or not author.strip():
        errors['author'] = "The 'Author' field cannot be empty."
    elif not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", author.strip()):
        errors[
            'author'] = "The 'Author' field must contain only letters and spaces."
    elif not (2 <= len(author.strip()) <= 40):
        errors[
            'author'] = "The 'Author' field must be between 2 and 40 characters long."

    # Text validation
    if not text or not text.strip():
        errors['text'] = "The 'Text' field cannot be empty."
    elif len(text.strip()) < 10:
        errors[
            'text'] = "The 'Text' field must be at least 10 characters long."

    # Date validation
    if not date or not date.strip():
        errors['date'] = "The 'Date' field cannot be empty."
    else:
        try:
            article_date = datetime.strptime(date, '%Y-%m-%d').date()
            if article_date > datetime.now().date():
                errors['date'] = "The date cannot be in the future."
        except ValueError:
            errors['date'] = "Incorrect date format. Use YYYY-MM-DD."

    # Link validation
    if not link or not link.strip():
        errors['link'] = "The 'Link' field cannot be empty."
    else:
        link_stripped = link.strip()
        if not (link_stripped.startswith(
                'http://') or link_stripped.startswith('https://')):
            errors[
                'link'] = "The link must start with 'http://' or 'https://'."
        else:
            # Check if there is something after http:// or https://
            if link_stripped == 'http://' or link_stripped == 'https://':
                errors[
                    'link'] = "The link must include a domain name after 'http://' or 'https://'."
            else:
                # Extract the part after the scheme for domain validation
                if link_stripped.startswith('http://'):
                    domain_part_with_path = link_stripped[7:]
                else:  # link_stripped.startswith('https://')
                    domain_part_with_path = link_stripped[8:]

                if not domain_part_with_path or domain_part_with_path.startswith(
                        '/'):
                    errors[
                        'link'] = "A valid domain name is required after 'http://' or 'https://'."
                else:
                    # Get only the domain name (before the first slash, if any)
                    domain_name = domain_part_with_path.split('/', 1)[0]
                    if not domain_name:  # Double check if domain name became empty after split
                        errors['link'] = "A valid domain name is required."
                    elif ' ' in domain_name:
                        errors[
                            'link'] = "The domain name in the link cannot contain spaces."
                    # Basic check for a dot in the domain name, or if it's 'localhost', or an IP address
                    # This is a simplified check and doesn't cover all valid domain/IP cases but catches common errors.
                    elif '.' not in domain_name and not (
                            domain_name.lower() == "localhost" or re.match(
                            r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$",
                            domain_name)):
                        errors[
                            'link'] = "The link does not appear to have a valid domain name (e.g., example.com or an IP address)."

        # Overall length check for the link
        if len(link_stripped) > 2048:
            # Ensure this error doesn't overwrite a more specific one if both conditions are met
            if 'link' not in errors:
                errors[
                    'link'] = "The link is too long (maximum 2048 characters)."
            elif "The link is too long" not in errors[
                'link']:  # Append if a different error is already there
                errors[
                    'link'] += " Also, the link is too long (maximum 2048 characters)."

    return errors

def add_article(title, author, text, date, link):
    """Adds a new article to the list and saves it."""
    articles_list = load_articles()
    new_article = {
        'title': title.strip(),
        'author': author.strip(),
        'text': text.strip(),
        'date': date.strip(),
        'link': link.strip()
    }
    articles_list.insert(0, new_article)
    save_articles(articles_list)
    return new_article

def delete_article(index):
    """Deletes an article by its index."""
    articles_list = load_articles()
    if 0 <= index < len(articles_list):
        del articles_list[index]
        save_articles(articles_list)
        return True
    return False