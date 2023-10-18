from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.utils.email_validator_adapter import EmailValidatorAdapter


def make_sut() -> EmailValidatorAdapter:
    return EmailValidatorAdapter()


class TestEmailValidatorAdapter(TestCase):

    def test_should_return_false_if_validator_returns_false(self):
        sut = make_sut()

        with patch.object(sut.__class__, 'is_valid', return_value=False):

            is_valid = sut.is_valid('invalid_email@email.com')
            self.assertEqual(is_valid, False)

    def test_should_return_true_if_validator_returns_true(self):
        sut = make_sut()

        with patch.object(sut.__class__, 'is_valid', return_value=True):

            is_valid = sut.is_valid('invalid_email@email.com')
            self.assertEqual(is_valid, True)

    def test_should_call_with_correct_email(self):
        sut = make_sut()

        sut.is_valid = MagicMock()

        sut.is_valid('valid_email@email.com')
        sut.is_valid.assert_called_with('valid_email@email.com')

