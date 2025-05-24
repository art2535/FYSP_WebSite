import unittest
from services.validation import validate_registration_form
from datetime import datetime

class TestValidationForm(unittest.TestCase):

    def setUp(self):
        self.base_form_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john.doe@example.com'
        }

    # Phone Validation Tests
    def test_validatePhone_Valid_1234567890_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)456-78-90'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertNotIn('phone', errors)

    def test_validatePhone_Valid_AllZeros_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(000)000-00-00'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertNotIn('phone', errors)

    def test_validatePhone_Valid_AllNines_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(999)999-99-99'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertNotIn('phone', errors)

    def test_validatePhone_Empty_ReturnsPhoneRequiredError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = ''
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone number is required.')

    def test_validatePhone_WrongCountryCode_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+1(123)456-78-90'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_TooShort_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(12)345-67-89'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_TooLong_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(1234)456-78-90'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_MissingParentheses_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7123456-78-90'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_MissingHyphens_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)4567890'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_NonDigit_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)45a-78-90'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_ExtraCharacters_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)456-78-90x'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    def test_validatePhone_WrongDigitCount_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['phone'] = '+7(123)4567-8-90'
        form_data['birthdate'] = '1990-05-15'
        errors = validate_registration_form(form_data)
        self.assertIn('phone', errors)
        self.assertEqual(errors['phone'], 'Phone must be in format +7(XXX)XXX-XX-XX.')

    # Birthdate Validation Tests
    def test_validateBirthdate_Valid_19900515_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '1990-05-15'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertNotIn('birthdate', errors)

    def test_validateBirthdate_Valid_20001231_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '2000-12-31'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertNotIn('birthdate', errors)

    def test_validateBirthdate_Valid_19700101_ReturnsNoError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '1970-01-01'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertNotIn('birthdate', errors)

    def test_validateBirthdate_Empty_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = ''
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertIn('birthdate', errors)
        self.assertEqual(errors['birthdate'], 'Invalid birthdate format.')

    def test_validateBirthdate_FutureDate_ReturnsFutureError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '2026-05-15'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertIn('birthdate', errors)
        self.assertEqual(errors['birthdate'], 'Birthdate cannot be in the future.')

    def test_validateBirthdate_WrongSeparator_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '1990/05/15'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertIn('birthdate', errors)
        self.assertEqual(errors['birthdate'], 'Invalid birthdate format.')

    def test_validateBirthdate_WrongOrder_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '15-05-1990'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertIn('birthdate', errors)
        self.assertEqual(errors['birthdate'], 'Invalid birthdate format.')

    def test_validateBirthdate_InvalidMonth_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '1990-13-15'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertIn('birthdate', errors)
        self.assertEqual(errors['birthdate'], 'Invalid birthdate format.')

    def test_validateBirthdate_InvalidDay_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '1990-05-32'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertIn('birthdate', errors)
        self.assertEqual(errors['birthdate'], 'Invalid birthdate format.')

    def test_validateBirthdate_NonNumeric_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '1990-ab-15'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertIn('birthdate', errors)
        self.assertEqual(errors['birthdate'], 'Invalid birthdate format.')

    def test_validateBirthdate_PartialDate_ReturnsFormatError(self):
        form_data = self.base_form_data.copy()
        form_data['birthdate'] = '1990-05'
        form_data['phone'] = '+7(123)456-78-90'
        errors = validate_registration_form(form_data)
        self.assertIn('birthdate', errors)
        self.assertEqual(errors['birthdate'], 'Invalid birthdate format.')

if __name__ == '__main__':
    unittest.main()