import unittest
from services.new_products_service import *  # путь подстрой под свой проект

class TestNewsValidation(unittest.TestCase):

    def test_all_fields_valid(self):
        """Все поля валидны — не должно быть ошибок"""
        errors = validate_news_form("Apple", "New iPhone released", "2025-05-26")
        self.assertEqual(errors, {})

    def test_missing_author(self):
        """Отсутствует автор"""
        errors = validate_news_form("", "Some text", "2025-05-26")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "The 'Brand / Name' field is required.")

    def test_missing_description(self):
        """Отсутствует описание"""
        errors = validate_news_form("Samsung", "", "2025-05-26")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "The 'Description' field is required.")

    def test_missing_date(self):
        """Отсутствует дата"""
        errors = validate_news_form("Sony", "Product info", "")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "The 'Date' field is required.")

    def test_invalid_date_format(self):
        """Неправильный формат даты"""
        errors = validate_news_form("Dell", "Laptop release", "26-05-2025")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "Invalid date format. Use YYYY-MM-DD.")

if __name__ == '__main__':
    unittest.main()

