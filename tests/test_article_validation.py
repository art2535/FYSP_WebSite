import unittest
from datetime import datetime, timedelta
from services.article_service import validate_article_form

class TestArticleValidation(unittest.TestCase):

    def test_all_fields_valid(self):
        """Тест: Все поля валидны."""
        errors = validate_article_form(
            title="Valid Title Here",
            author="Valid Author",
            text="This is a valid text for the article, long enough.",
            date="2023-01-01",
            link="http://example.com"
        )
        self.assertEqual(errors, {})

    # --- Тесты для поля 'Title' ---
    def test_title_empty(self):
        """Тест: Поле 'Title' пустое."""
        errors = validate_article_form("", "Author", "Some text", "2023-01-01", "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'], "The 'Title' field cannot be empty.")

    def test_title_too_short(self):
        """Тест: Поле 'Title' слишком короткое."""
        errors = validate_article_form("Short", "Author", "Some text", "2023-01-01", "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'], "The 'Title' field must be longer than 5 characters.")

    def test_title_too_long(self):
        """Тест: Поле 'Title' слишком длинное."""
        long_title = "a" * 51
        errors = validate_article_form(long_title, "Author", "Some text", "2023-01-01", "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'], "The 'Title' field cannot exceed 50 characters.")

    def test_title_whitespace_only(self):
        """Тест: Поле 'Title' состоит только из пробелов."""
        errors = validate_article_form("     ", "Author", "Some text", "2023-01-01", "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'], "The 'Title' field cannot be empty.")

    # --- Тесты для поля 'Author' ---
    def test_author_empty(self):
        """Тест: Поле 'Author' пустое."""
        errors = validate_article_form("Valid Title", "", "Some text", "2023-01-01", "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "The 'Author' field cannot be empty.")

    def test_author_whitespace_only(self):
        """Тест: Поле 'Author' состоит только из пробелов."""
        errors = validate_article_form("Valid Title", "   ", "Some text", "2023-01-01", "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "The 'Author' field cannot be empty.")

    def test_author_invalid_chars(self):
        """Тест: Поле 'Author' содержит недопустимые символы."""
        errors = validate_article_form("Valid Title", "Author123", "Some text", "2023-01-01", "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "The 'Author' field must contain only letters and spaces.")
        errors = validate_article_form("Valid Title", "Author!", "Some text", "2023-01-01", "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "The 'Author' field must contain only letters and spaces.")

    def test_author_too_short(self): # В коде указано (1 <= len <= 40), так что тест на <1 не нужен, если поле не пустое
        """Тест: Поле 'Author' слишком короткое (нет отдельного правила, но пустое уже проверяется)."""
        # Валидация (1 <= len(author.strip()) <= 40) означает, что пустая строка после strip() не пройдет.
        # Этот случай покрывается тестом test_author_empty
        pass

    def test_author_too_long(self):
        """Тест: Поле 'Author' слишком длинное."""
        long_author = "a" * 41
        errors = validate_article_form("Valid Title", long_author, "Some text", "2023-01-01", "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "The 'Author' field must be between 1 and 40 characters long.")

    def test_author_valid_cyrillic(self):
        """Тест: Поле 'Author' с кириллицей."""
        errors = validate_article_form("Valid Title", "Автор Тест", "Some text", "2023-01-01", "http://example.com")
        self.assertNotIn('author', errors)

    # --- Тесты для поля 'Text' ---
    def test_text_empty(self):
        """Тест: Поле 'Text' пустое."""
        errors = validate_article_form("Valid Title", "Author", "", "2023-01-01", "http://example.com")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "The 'Text' field cannot be empty.")

    def test_text_whitespace_only(self):
        """Тест: Поле 'Text' состоит только из пробелов."""
        errors = validate_article_form("Valid Title", "Author", "       ", "2023-01-01", "http://example.com")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "The 'Text' field cannot be empty.")

    def test_text_too_short(self):
        """Тест: Поле 'Text' слишком короткое."""
        errors = validate_article_form("Valid Title", "Author", "Too short", "2023-01-01", "http://example.com")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "The 'Text' field must be at least 10 characters long.")

    # --- Тесты для поля 'Date' ---
    def test_date_empty(self):
        """Тест: Поле 'Date' пустое."""
        errors = validate_article_form("Valid Title", "Author", "Valid text content", "", "http://example.com")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "The 'Date' field cannot be empty.")

    def test_date_invalid_format(self):
        """Тест: Поле 'Date' имеет неверный формат."""
        errors = validate_article_form("Valid Title", "Author", "Valid text content", "01-01-2023", "http://example.com")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "Incorrect date format. Use YYYY-MM-DD.")
        errors = validate_article_form("Valid Title", "Author", "Valid text content", "2023/01/01", "http://example.com")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "Incorrect date format. Use YYYY-MM-DD.")

    def test_date_in_future(self):
        """Тест: Поле 'Date' указывает на будущую дату."""
        future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        errors = validate_article_form("Valid Title", "Author", "Valid text content", future_date, "http://example.com")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "The date cannot be in the future.")

    def test_date_valid_past(self):
        """Тест: Поле 'Date' с валидной прошедшей датой."""
        past_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        errors = validate_article_form("Valid Title", "Author", "Valid text content", past_date, "http://example.com")
        self.assertNotIn('date', errors)

    def test_date_valid_today(self):
        """Тест: Поле 'Date' с сегодняшней датой."""
        today_date = datetime.now().strftime('%Y-%m-%d')
        errors = validate_article_form("Valid Title", "Author", "Valid text content", today_date, "http://example.com")
        self.assertNotIn('date', errors)

    # --- Тесты для поля 'Link' ---
    def test_link_empty(self):
        """Тест: Поле 'Link' пустое."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The 'Link' field cannot be empty.")

    def test_link_whitespace_only(self):
        """Тест: Поле 'Link' состоит только из пробелов."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "   ")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The 'Link' field cannot be empty.")

    def test_link_no_protocol(self):
        """Тест: Поле 'Link' без http:// или https://."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "example.com")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The link must start with 'http://' or 'https://'.")

    def test_link_protocol_only_http(self):
        """Тест: Поле 'Link' содержит только http://."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "http://")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The link must include a domain name after 'http://' or 'https://'.")

    def test_link_protocol_only_https(self):
        """Тест: Поле 'Link' содержит только https://."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "https://")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The link must include a domain name after 'http://' or 'https://'.")

    def test_link_protocol_with_slash_no_domain(self):
        """Тест: Поле 'Link' с протоколом и слешем, но без домена."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "https:///")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "A valid domain name is required after 'http://' or 'https://'.")

    def test_link_domain_with_space(self):
        """Тест: Поле 'Link' содержит пробел в доменном имени."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "http://exam ple.com")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The domain name in the link cannot contain spaces.")

    def test_link_no_dot_in_domain(self):
        """Тест: Поле 'Link' не содержит точки в домене (и не localhost/IP)."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "http://example")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The link does not appear to have a valid domain name (e.g., example.com or an IP address).")

    def test_link_too_long(self):
        """Тест: Поле 'Link' слишком длинное."""
        long_link = "http://" + "a" * 2040 + ".com" # http:// + 2040 'a's + .com = 7 + 2040 + 4 = 2051
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", long_link)
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The link is too long (maximum 2048 characters).")

    def test_link_valid_http(self):
        """Тест: Валидная ссылка с http://."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "http://example.com/page")
        self.assertNotIn('link', errors)

    def test_link_valid_https(self):
        """Тест: Валидная ссылка с https://."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "https://sub.example.co.uk/path?query=param#fragment")
        self.assertNotIn('link', errors)


    def test_link_valid_ip(self):
        """Тест: Валидная ссылка с IP-адресом."""
        errors = validate_article_form("Valid Title", "Author", "Valid text", "2023-01-01", "http://127.0.0.1/path")
        self.assertNotIn('link', errors)

    # --- Тесты на комбинацию ошибок ---
    def test_all_fields_empty(self):
        """Тест: Все поля пустые."""
        errors = validate_article_form("", "", "", "", "")
        self.assertIn('title', errors)
        self.assertIn('author', errors)
        self.assertIn('text', errors)
        self.assertIn('date', errors)
        self.assertIn('link', errors)

if __name__ == '__main__':
    unittest.main()