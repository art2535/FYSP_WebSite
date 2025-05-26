import unittest
from services.validation import validate_partner_form

class TestPartnerValidationForm(unittest.TestCase):
    def setUp(self):
        self.base_form_data = {
            'name': 'Tech Corp',
            'description': 'Innovative tech solutions for all.',
            'phone': '+7(123)456-78-90',
            'date': '2023-05-15'
        }

    # Name Validation Tests
    def test_validateName_Valid_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['name'] = 'Acme Inc.'
        errors = validate_partner_form(form_data)
        self.assertNotIn('name', errors)

    def test_validateName_Valid_WithPunctuation_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['name'] = 'A & B Co., Ltd.'
        errors = validate_partner_form(form_data)
        self.assertNotIn('name', errors)

    def test_validateName_Empty_ReturnsRequiredError(self):
        form_data = self.base_form_data.copy()
        form_data['name'] = ''
        errors = validate_partner_form(form_data)
        self.assertIn('name', errors)
        self.assertEqual(errors['name'], 'Company name is required.')

    def test_validateName_TooShort_ReturnsMinLengthError(self):
        form_data = self.base_form_data.copy()
        form_data['name'] = 'Ab'
        errors = validate_partner_form(form_data)
        self.assertIn('name', errors)
        self.assertEqual(errors['name'], 'Company name must be at least 3 characters.')

    def test_validateName_TooLong_ReturnsMaxLengthError(self):
        form_data = self.base_form_data.copy()
        form_data['name'] = 'A' * 101
        errors = validate_partner_form(form_data)
        self.assertIn('name', errors)
        self.assertEqual(errors['name'], 'Company name cannot exceed 100 characters.')

    def test_validateName_InvalidCharacters_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['name'] = 'Company#123'
        errors = validate_partner_form(form_data)
        self.assertIn('name', errors)
        self.assertEqual(errors['name'], 'Name can only contain letters, numbers, spaces, and basic punctuation.')

    # Description Validation Tests
    def test_validateDescription_Valid_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['description'] = 'Providing cutting-edge technology solutions.'
        errors = validate_partner_form(form_data)
        self.assertNotIn('description', errors)

    def test_validateDescription_Empty_ReturnsRequiredError(self):
        form_data = self.base_form_data.copy()
        form_data['description'] = ''
        errors = validate_partner_form(form_data)
        self.assertIn('description', errors)
        self.assertEqual(errors['description'], 'Description is required.')

    def test_validateDescription_TooShort_ReturnsMinLengthError(self):
        form_data = self.base_form_data.copy()
        form_data['description'] = 'Too short'
        errors = validate_partner_form(form_data)
        self.assertIn('description', errors)
        self.assertEqual(errors['description'], 'Description must be at least 10 characters.')

    def test_validateDescription_TooLong_ReturnsMaxLengthError(self):
        form_data = self.base_form_data.copy()
        form_data['description'] = 'A' * 501
        errors = validate_partner_form(form_data)
        self.assertIn('description', errors)
        self.assertEqual(errors['description'], 'Description cannot exceed 500 characters.')

    # Phone Validation Tests
    def test_validatePhone_Valid_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_partner_form(form_data)
        self.assertNotIn('phone', errors)

    def test_validatePhone_Valid_AllZeros_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(000)000-00-00'
        errors = validate_partner_form(form_data)
        self.assertNotIn('phone', errors)

    def test_validatePhone_Valid_AllNines_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(999)999-99-99'
        errors = validate_partner_form(form_data)
        self.assertNotIn('phone', errors)

    def test_validatePhone_Empty_ReturnsRequiredError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = ''
        errors = validate_partner_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone number is required.')

    def test_validatePhone_WrongCountryCode_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+1(123)456-78-90'
        errors = validate_partner_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_TooShort_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(12)345-67-89'
        errors = validate_partner_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_TooLong_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(1234)456-78-90'
        errors = validate_partner_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_MissingParentheses_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7123456-78-90'
        errors = validate_partner_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_MissingHyphens_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)4567890'
        errors = validate_partner_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_NonDigit_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)45a-78-90'
        errors = validate_partner_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_ExtraCharacters_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)456-78-90x'
        errors = validate_partner_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    # Date Validation Tests
    def test_validateDate_Valid_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = '2023-05-15'
        errors = validate_partner_form(form_data)
        self.assertNotIn('date', errors)

    def test_validateDate_Valid_OldDate_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = '2000-01-01'
        errors = validate_partner_form(form_data)
        self.assertNotIn('date', errors)

    def test_validateDate_Empty_ReturnsRequiredError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = ''
        errors = validate_partner_form(form_data)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], 'Date is required.')

    def test_validateDate_FutureDate_ReturnsFutureError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = '2026-05-15'
        errors = validate_partner_form(form_data)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], 'Date cannot be in the future.')

    def test_validateDate_InvalidFormat_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = '2023/05/15'
        errors = validate_partner_form(form_data)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], 'Invalid date format.')

    def test_validateDate_InvalidMonth_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = '2023-13-15'
        errors = validate_partner_form(form_data)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], 'Invalid date format.')

    def test_validateDate_InvalidDay_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = '2023-05-32'
        errors = validate_partner_form(form_data)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], 'Invalid date format.')

    def test_validateDate_NonNumeric_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = '2023-ab-15'
        errors = validate_partner_form(form_data)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], 'Invalid date format.')

    def test_validateDate_PartialDate_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['date'] = '2023-05'
        errors = validate_partner_form(form_data)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], 'Invalid date format.')

if __name__ == '__main__':
    unittest.main()