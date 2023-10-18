from email_validator import validate_email, EmailNotValidError

from src.presentation.protocols.email_validator import EmailValidator


class EmailValidatorAdapter(EmailValidator):
    def is_valid(self, email: str) -> bool | str:
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
