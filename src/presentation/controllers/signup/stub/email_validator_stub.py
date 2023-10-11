from src.presentation.protocols.email_validator import EmailValidator


class EmailValidatorStub(EmailValidator):
    def is_valid(self, email: str) -> bool:
        return True



