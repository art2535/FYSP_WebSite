import unittest
from datetime import datetime, timedelta
from services.article_service import validate_article_form


class TestArticleValidation(unittest.TestCase):

    # --- Тесты для поля "Заголовок (title)" ---
    def test_validateTitle_ValidInput_NoError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertNotIn('title', errors)

    def test_validateTitle_Empty_ReturnsEmptyError(self):
        errors = validate_article_form("", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'], "The 'Title' field cannot be empty.")

    def test_validateTitle_TooShort_ReturnsMinLengthError(self):
        errors = validate_article_form("Short", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'],
                         "The 'Title' must be longer than 5 characters.")

    def test_validateTitle_TooLong_ReturnsMaxLengthError(self):
        long_title = "a" * 51
        errors = validate_article_form(long_title, "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'],
                         "The 'Title' must not exceed 50 characters.")

    def test_validateTitle_ExactlyMinBoundaryInvalid_ReturnsMinLengthError(
            self):
        # Граничное значение, должно быть невалидным (нужно > 5)
        errors = validate_article_form("FiveC", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'],
                         "The 'Title' must be longer than 5 characters.")

    def test_validateTitle_ExactlyMinBoundaryValid_NoError(self):
        # Граничное значение, должно быть валидным
        errors = validate_article_form("SixCha", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertNotIn('title', errors)

    def test_validateTitle_ExactlyMaxBoundaryValid_NoError(self):
        # Граничное значение, должно быть валидным
        title_50 = "a" * 50
        errors = validate_article_form(title_50, "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertNotIn('title', errors)

    def test_validateTitle_SpacesOnly_ReturnsEmptyError(self):
        errors = validate_article_form("     ", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('title', errors)
        self.assertEqual(errors['title'], "The 'Title' field cannot be empty.")

    # --- Тесты для поля "Автор (author)" ---
    def test_validateAuthor_ValidInput_NoError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertNotIn('author', errors)

    def test_validateAuthor_Empty_ReturnsEmptyError(self):
        errors = validate_article_form("Valid Title", "",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'],
                         "The 'Author' field cannot be empty.")

    def test_validateAuthor_WithNumbers_ReturnsLettersAndSpacesError(self):
        errors = validate_article_form("Valid Title", "Author123",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'],
                         "The 'Author' field must contain only letters and spaces.")

    def test_validateAuthor_WithSpecialChars_ReturnsLettersAndSpacesError(
            self):
        errors = validate_article_form("Valid Title", "Author!",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'],
                         "The 'Author' field must contain only letters and spaces.")

    def test_validateAuthor_TooShort_ReturnsLengthRangeError(self):
        errors = validate_article_form("Valid Title", "A",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'],
                         "The 'Author' must be between 2 and 40 characters.")

    def test_validateAuthor_ExactlyMinBoundaryValid_NoError(self):
        errors = validate_article_form("Valid Title", "Jo",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertNotIn('author', errors)

    def test_validateAuthor_TooLong_ReturnsLengthRangeError(self):
        long_author = "a" * 41
        errors = validate_article_form("Valid Title", long_author,
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'],
                         "The 'Author' must be between 2 and 40 characters.")

    def test_validateAuthor_ExactlyMaxBoundaryValid_NoError(self):
        author_40 = "FirstName LastName MiddleName Patronymic"[:40]
        errors = validate_article_form("Valid Title", author_40,
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertNotIn('author', errors,
                         f"Author '{author_40}' with length {len(author_40)} was unexpectedly invalid.")

    def test_validateAuthor_SpacesOnly_ReturnsEmptyError(self):
        errors = validate_article_form("Valid Title", "   ",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertIn('author', errors)
        self.assertEqual(errors['author'],
                         "The 'Author' field cannot be empty.")

    # --- Тесты для поля "Текст (text)" ---
    def test_validateText_ValidInput_NoError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "This is a valid text content.",
                                       "2023-01-01", "http://example.com")
        self.assertNotIn('text', errors)

    def test_validateText_Empty_ReturnsEmptyError(self):
        errors = validate_article_form("Valid Title", "Valid Author", "",
                                       "2023-01-01", "http://example.com")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "The 'Text' field cannot be empty.")

    def test_validateText_TooShort_ReturnsMinLengthError(self):
        errors = validate_article_form("Valid Title", "Valid Author", "Short",
                                       "2023-01-01", "http://example.com")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'],
                         "The 'Text' must be at least 10 characters long.")

    def test_validateText_ExactlyMinBoundaryInvalid_ReturnsMinLengthError(
            self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "NineChars", "2023-01-01",
                                       "http://example.com")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'],
                         "The 'Text' must be at least 10 characters long.")

    def test_validateText_ExactlyMinBoundaryValid_NoError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "TenChars10", "2023-01-01",
                                       "http://example.com")
        self.assertNotIn('text', errors)

    def test_validateText_SpacesOnly_ReturnsEmptyError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "          ", "2023-01-01",
                                       "http://example.com")
        self.assertIn('text', errors)
        self.assertEqual(errors['text'], "The 'Text' field cannot be empty.")

    # --- Тесты для поля "Дата (date)" ---
    def test_validateDate_ValidPastDate_NoError(self):
        valid_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", valid_date,
                                       "http://example.com")
        self.assertNotIn('date', errors)

    def test_validateDate_Empty_ReturnsEmptyError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "",
                                       "http://example.com")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "The 'Date' field cannot be empty.")

    def test_validateDate_InvalidFormat_ReturnsFormatError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "01-01-2023",
                                       "http://example.com")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'],
                         "Invalid date format. Use YYYY-MM-DD.")

    def test_validateDate_FutureDate_ReturnsFutureDateError(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", future_date,
                                       "http://example.com")
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "The date cannot be in the future.")

    def test_validateDate_TodayDate_NoError(self):
        today_date = datetime.now().strftime('%Y-%m-%d')
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", today_date,
                                       "http://example.com")
        self.assertNotIn('date', errors)

    # --- Тесты для поля "Ссылка (link)" ---
    def test_validateLink_ValidHttp_NoError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.com")
        self.assertNotIn('link', errors)

    def test_validateLink_ValidHttps_NoError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "https://sub.example.co.uk/path?query=value")
        self.assertNotIn('link', errors)

    def test_validateLink_ValidLocalhostWithPortAndPath_NoError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://localhost:8080/path")
        self.assertNotIn('link', errors)

    def test_validateLink_ValidIpWithPortAndPath_NoError(
            self):  # Assuming IP can have port and path
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://192.168.1.1:80/path")
        self.assertNotIn('link', errors)

    def test_validateLink_Empty_ReturnsEmptyError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01", "")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The 'Link' field cannot be empty.")

    def test_validateLink_SpacesOnly_ReturnsEmptyError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "   ")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'], "The 'Link' field cannot be empty.")

    def test_validateLink_NoScheme_ReturnsSchemeError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "example.com")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "The link must start with 'http://' or 'https://'.")

    def test_validateLink_InvalidScheme_ReturnsSchemeError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "ftp://example.com")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "The link must start with 'http://' or 'https://'.")

    def test_validateLink_HttpSchemeOnly_ReturnsDomainNameAfterSchemeError(
            self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "The link must contain a domain name after the scheme.")

    def test_validateLink_HttpsSchemeOnly_ReturnsDomainNameAfterSchemeError(
            self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "https://")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "The link must contain a domain name after the scheme.")

    def test_validateLink_SchemeWithSlashNoDomain_ReturnsValidDomainRequiredError(
            self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http:///path")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "A valid domain name is required after 'http://' or 'https://'.")

    def test_validateLink_NoDomainNameBeforeTld_ReturnsInvalidDomainStructureError(
            self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://.com")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "Invalid domain structure (e.g., example.com).")

    def test_validateLink_DomainWithSpaces_ReturnsDomainCannotContainSpacesError(
            self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://exam ple.com")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "The domain name cannot contain spaces.")

    def test_validateLink_NoTld_ReturnsValidDomainNameError(
            self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "The link must contain a valid domain name (e.g., example.com).")

    def test_validateLink_ShortTld_ReturnsTldMinLengthError(self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.c")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "Top-level domain must be at least 2 characters.")

    def test_validateLink_DomainEndsWithDot_ReturnsInvalidDomainStructureError(
            self):
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       "http://example.")
        self.assertIn('link', errors)
        self.assertEqual(errors['link'],
                         "Invalid domain structure (e.g., example.com).")

    def test_validateLink_TooLong_ReturnsMaxLengthError(self):
        long_link = "http://" + "a" * 2040 + ".com"  # 7 + 2040 + 4 = 2051
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       long_link)
        self.assertIn('link', errors)
        self.assertTrue("too long" in errors[
            'link'].lower())

    def test_validateLink_ExactlyMaxBoundaryValid_NoError(self):
        # 7 (http://) + x + 4 (.com) = 2048 => x = 2037
        link_2048 = "http://" + "a" * 2037 + ".com"
        errors = validate_article_form("Valid Title", "Valid Author",
                                       "Valid text content.", "2023-01-01",
                                       link_2048)
        self.assertNotIn('link', errors,
                         f"Link with length {len(link_2048)} was unexpectedly invalid.")

    # --- Тесты для всех полей одновременно ---
    def test_validateAllFields_AllEmpty_ReturnsMultipleErrors(self):
        errors = validate_article_form("", "", "", "", "")
        self.assertIn('title', errors)
        self.assertIn('author', errors)
        self.assertIn('text', errors)
        self.assertIn('date', errors)
        self.assertIn('link', errors)


if __name__ == '__main__':
    unittest.main()