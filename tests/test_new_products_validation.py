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

if __name__ == '__main__':
    unittest.main()
