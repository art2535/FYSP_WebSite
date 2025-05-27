import unittest
import os
from datetime import datetime

from services.reviews_service import (
    validate_review,
    add_review,
    get_reviews,
    get_products,
    reviews_data
)


class TestReviewLogic(unittest.TestCase):
    """
    Unit tests for the reviews_service module functions:
    - validate_review: Validate review input data
    - add_review: Add a new review
    - get_reviews: Retrieve reviews with optional filtering and sorting
    - get_products: Retrieve the list of products

    The shared reviews_data dict is cleared before each test to ensure test isolation.
    """

    def setUp(self):
        """
        Clears the shared reviews_data dict before each test to avoid data leakage
        between tests and maintain independence.
        """
        reviews_data.clear()


    def test_validate_review_empty_nickname(self):
        """
        Tests that an error is returned when the nickname is empty.
        """
        errors = validate_review('', 'company', '3', 'Good text', None)
        self.assertIn("Nickname is required.", errors)

    def test_validate_review_short_nickname(self):
        """
        Tests that an error is returned when the nickname is shorter than 2 characters.
        """
        errors = validate_review('a', 'company', '3', 'Good text', None)
        self.assertIn("Nickname must be at least 2 characters long.", errors)

    def test_validate_review_long_nickname(self):
        """
        Tests that an error is returned when the nickname is longer than 20 characters.
        """
        errors = validate_review('a' * 21, 'company', '3', 'Good text', None)
        self.assertIn("Nickname cannot be longer than 20 characters.", errors)

    def test_validate_review_nickname_no_letters(self):
        """
        Tests that an error is returned if the nickname does not contain at least one letter.
        """
        errors = validate_review('123456', 'company', '3', 'Good text', None)
        self.assertIn("Nickname must contain at least one letter.", errors)

    def test_validate_review_nickname_with_special_chars(self):
        """
        Tests that an error is returned if the nickname contains special characters.
        """
        errors = validate_review('abc!', 'company', '3', 'Good text', None)
        self.assertIn("Nickname can only contain letters and numbers, no special characters.", errors)

    def test_validate_review_rating_not_number(self):
        """
        Tests that an error is returned if the rating is not a valid number.
        """
        errors = validate_review('validnick', 'company', 'abc', 'Good text', None)
        self.assertIn("Rating must be a valid number.", errors)

    def test_validate_review_rating_too_low(self):
        """
        Tests that an error is returned if the rating is less than 1.
        """
        errors = validate_review('validnick', 'company', '0', 'Good text', None)
        self.assertIn("Rating must be a number between 1 and 5.", errors)

    def test_validate_review_rating_too_high(self):
        """
        Tests that an error is returned if the rating is greater than 5.
        """
        errors = validate_review('validnick', 'company', '6', 'Good text', None)
        self.assertIn("Rating must be a number between 1 and 5.", errors)

    def test_validate_review_empty_text(self):
        """
        Tests that an error is returned if the review text is empty.
        """
        errors = validate_review('validnick', 'company', '3', '', None)
        self.assertIn("Review text is required.", errors)

    def test_validate_review_text_too_long(self):
        """
        Tests that an error is returned if the review text exceeds 150 characters.
        """
        errors = validate_review('validnick', 'company', '3', 'a' * 151, None)
        self.assertIn("Review text cannot exceed 150 characters.", errors)

    def test_validate_review_text_less_than_3_letters(self):
        """
        Tests that an error is returned if the review text contains fewer than 3 letters.
        """
        errors = validate_review('validnick', 'company', '3', '12a', None)
        self.assertIn("Review text must contain at least 3 letters.", errors)

    def test_validate_review_text_only_digits_and_special(self):
        """
        Tests that an error is returned if the review text consists only of digits or special characters.
        """
        errors = validate_review('validnick', 'company', '3', '123!!!', None)
        self.assertIn("Review text cannot consist only of digits or special characters.", errors)

    def test_validate_review_product_category_no_product_id(self):
        """
        Tests that an error is returned if category is 'product' but product_id is missing.
        """
        errors = validate_review('validnick', 'product', '3', 'Good text', '')
        self.assertIn("Please select a valid product.", errors)

    def test_validate_review_product_category_invalid_product_id(self):
        """
        Tests that an error is returned if category is 'product' but product_id is invalid.
        """
        errors = validate_review('validnick', 'product', '3', 'Good text', '9999')
        self.assertIn("Please select a valid product.", errors)

    def test_add_review_success_company(self):
        """
        Tests successful addition of a review for category 'company'.
        """
        success, errors = add_review('validuser', 'company', '5', 'Great product!', None)
        self.assertTrue(success)
        self.assertIsNone(errors)
        self.assertIn('validuser', reviews_data)
        self.assertEqual(len(reviews_data['validuser']), 1)

    def test_add_review_success_product(self):
        """
        Tests successful addition of a review for category 'product' with a valid product_id.
        """
        success, errors = add_review('validuser2', 'product', '4', 'Nice product!', '1')
        self.assertTrue(success)
        self.assertIsNone(errors)
        added = reviews_data['validuser2'][0]
        self.assertEqual(added['product_id'], '1')
        self.assertEqual(added['product_name'], 'Processor Intel Core i7 14700KF LGA1700 OEM')

    def test_add_review_failure(self):
        """
        Tests that adding a review fails with multiple validation errors.
        """
        success, errors = add_review('', 'company', '10', '', None)
        self.assertFalse(success)
        self.assertIn("Nickname is required.", errors)
        self.assertIn("Rating must be a number between 1 and 5.", errors)
        self.assertIn("Review text is required.", errors)

    def test_get_reviews_filter_category(self):
        """
        Tests filtering of reviews by category.
        """
        reviews_data.update({
            'user1': [{'category': 'company', 'rating': 3, 'text': 'Good', 'date': '2025-05-24'}],
            'user2': [{'category': 'product', 'rating': 5, 'text': 'Excellent', 'date': '2025-05-26'}],
            'user3': [{'category': 'company', 'rating': 2, 'text': 'Bad', 'date': '2025-05-25'}],
        })
        company_reviews = get_reviews(filter_category='company')
        self.assertEqual(len(company_reviews), 2)
        self.assertTrue(all(r['category'] == 'company' for r in company_reviews))

    def test_get_reviews_no_filter(self):
        """
        Tests retrieval of all reviews without filtering.
        """
        reviews_data.update({
            'user1': [{'category': 'company', 'rating': 3, 'text': 'Good', 'date': '2025-05-24'}],
            'user2': [{'category': 'product', 'rating': 5, 'text': 'Excellent', 'date': '2025-05-26'}],
            'user3': [{'category': 'company', 'rating': 2, 'text': 'Bad', 'date': '2025-05-25'}],
        })
        all_reviews = get_reviews()
        self.assertEqual(len(all_reviews), 3)

    def test_get_reviews_sort_newest(self):
        """
        Tests sorting of reviews by newest date first.
        """
        reviews_data.update({
            'user1': [{'category': 'company', 'rating': 3, 'text': 'Good', 'date': '2025-05-24'}],
            'user2': [{'category': 'product', 'rating': 5, 'text': 'Excellent', 'date': '2025-05-26'}],
            'user3': [{'category': 'company', 'rating': 2, 'text': 'Bad', 'date': '2025-05-25'}],
        })
        sorted_new = get_reviews(sort_order='new')
        dates = [r['date'] for r in sorted_new]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_get_reviews_sort_oldest(self):
        """
        Tests sorting of reviews by oldest date first.
        """
        reviews_data.update({
            'user1': [{'category': 'company', 'rating': 3, 'text': 'Good', 'date': '2025-05-24'}],
            'user2': [{'category': 'product', 'rating': 5, 'text': 'Excellent', 'date': '2025-05-26'}],
            'user3': [{'category': 'company', 'rating': 2, 'text': 'Bad', 'date': '2025-05-25'}],
        })
        sorted_old = get_reviews(sort_order='old')
        dates = [r['date'] for r in sorted_old]
        self.assertEqual(dates, sorted(dates))

    def test_get_products_returns_list(self):
        """
        Tests that get_products returns a non-empty list of products
        and that each product has a 'name' key.
        """
        prods = get_products()
        self.assertIsInstance(prods, list)
        self.assertGreater(len(prods), 0)
        self.assertIn('name', prods[0])


if __name__ == '__main__':
    unittest.main()


