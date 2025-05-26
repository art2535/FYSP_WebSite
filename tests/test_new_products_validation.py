from datetime import datetime, timedelta
import unittest
from services.new_products_service import *

class TestNewsValidation(unittest.TestCase):

    def test_all_fields_valid(self):
        errors = validate_news_form("Apple", "New iPhone released", "2025-05-26")
        self.assertEqual(errors, {})

    def test_missing_author(self):
        errors = validate_news_form("", "Some text", "2025-05-26")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "The 'Brand / Name' field is required.")

    def test_missing_description(self):
        errors = validate_news_form("Samsung", "", "2025-05-26")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "The 'Description' field is required.")

    def test_missing_date(self):
        errors = validate_news_form("Sony", "Product info", "")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "The 'Date' field is required.")

    def test_invalid_date_format(self):
        errors = validate_news_form("Dell", "Laptop release", "26-05-2025")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "Invalid date format. Use YYYY-MM-DD.")

    def test_date_more_than_one_year_future(self):
        """Дата больше чем через 1 год от текущей"""
        future_date = (datetime.today() + timedelta(days=380)).strftime('%Y-%m-%d')
        errors = validate_news_form("FutureBrand", "Future product", future_date)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "Date must be within one year from today.")

    def test_date_more_than_one_year_past(self):
        """Дата более чем год назад"""
        past_date = (datetime.today() - timedelta(days=380)).strftime('%Y-%m-%d')
        errors = validate_news_form("OldBrand", "Old product", past_date)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "Date must be within one year from today.")
        
    def test_author_too_short(self):
        errors = validate_news_form("AB", "Good product", "2025-05-26")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "Brand / Name must be at least 5 characters.")

    def test_text_too_short(self):
        errors = validate_news_form("Lenovo", "123", "2025-05-26")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "Description must be at least 5 characters.")

    def test_author_too_long(self):
        long_author = "A" * 101
        errors = validate_news_form(long_author, "Decent product", "2025-05-26")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "Brand / Name must be less than 100 characters..")

    def test_text_too_long(self):
        long_text = "X" * 201
        errors = validate_news_form("CoolerMaster", long_text, "2025-05-26")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "Description must not exceed 200 characters.")

    def test_author_is_only_digits(self):
        errors = validate_news_form("123456", "Nice product", "2025-05-26")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "Brand / Name cannot be only numbers.")

    def test_text_is_only_digits(self):
        errors = validate_news_form("Gigabyte", "123456", "2025-05-26")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "Description cannot be only numbers.")

    def test_author_is_spaces_only(self):
        errors = validate_news_form("     ", "Some description", "2025-05-26")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'], "The 'Brand / Name' field is required.")

    def test_text_is_spaces_only(self):
        errors = validate_news_form("ASUS", "     ", "2025-05-26")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "The 'Description' field is required.")

    def test_all_fields_empty_strings(self):
        errors = validate_news_form("", "", "")
        self.assertIn('author', errors)
        self.assertIn('text', errors)
        self.assertIn('date', errors)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
