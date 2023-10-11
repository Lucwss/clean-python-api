import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from src.domain.models.account import AccountModel
from src.domain.usecases.add_account import AddAccount, AddAccountModel
from src.presentation.controllers.signup.signup import SignUpController
from src.presentation.controllers.signup.stub.add_account_stub import AddAccountStubStub
from src.presentation.controllers.signup.stub.email_validator_stub import EmailValidatorStub
from src.presentation.errors.invalid_param_error import InvalidParamError
from src.presentation.errors.missing_param_error import MissingParamError
from src.presentation.errors.server_error import ServerError
from src.presentation.protocols.email_validator import EmailValidator
from src.presentation.protocols.http import HttpRequest
from src.presentation.protocols.interface import BaseInterface


class SutTypes(BaseInterface):
    email_validator_stub: EmailValidator
    add_account_stub: AddAccount
    sut: SignUpController


def make_email_validator() -> EmailValidator:
    return EmailValidatorStub()


def make_add_account() -> AddAccount:
    return AddAccountStubStub()


def make_sut() -> SutTypes:
    email_validator_stub = make_email_validator()
    add_account_stub = make_add_account()
    sut = SignUpController(email_validator_stub, add_account_stub)
    return SutTypes(email_validator_stub=email_validator_stub, sut=sut, add_account_stub=add_account_stub)


events = []


class TestSignup(IsolatedAsyncioTestCase):

    def setUp(self):
        events.append("setUp")

    async def test_should_return_400_if_no_name_is_provided(self):
        sut = make_sut().sut

        http_request = {
            "body": {
                "email": "any_email",
                "password": "any_password",
                "password_confirmation": "any_password"
            }
        }

        http_response = await sut.handle(HttpRequest(**http_request))
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, MissingParamError('name'))
        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_400_if_no_email_is_provided(self):
        sut = make_sut().sut

        http_request = {
            "body": {
                "name": "any_name",
                "password": "any_password",
                "password_confirmation": "any_password"
            }
        }

        http_response = await sut.handle(HttpRequest(**http_request))
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, MissingParamError('email'))
        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_400_if_no_password_is_provided(self):
        sut = make_sut().sut

        http_request = {
            "body": {
                "name": "any_name",
                "email": "any_email",
                "password_confirmation": "any_password"
            }
        }

        http_response = await sut.handle(HttpRequest(**http_request))
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, MissingParamError('password'))
        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_400_if_no_confirmation_is_provided(self):
        sut = make_sut().sut

        http_request = {
            "body": {
                "name": "any_name",
                "email": "any_email",
                "password": "any_password"
            }
        }

        http_response = await sut.handle(HttpRequest(**http_request))
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, MissingParamError('password_confirmation'))
        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_400_if_password_confirmation_fails(self):
        sut = make_sut().sut
        http_request = {
            "body": {
                "name": "any_name",
                "email": "any_email",
                "password": "any_password",
                "password_confirmation": "other_password"
            }
        }

        http_response = await sut.handle(HttpRequest(**http_request))
        self.assertEqual(http_response.status_code, 400)
        self.assertEqual(http_response.body, InvalidParamError('password_confirmation'))
        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_400_if_an_invalid_email_is_provided(self):
        sut_instance = make_sut()
        sut = sut_instance.sut

        email_validator_stub = sut_instance.email_validator_stub

        with patch.object(email_validator_stub.__class__, 'is_valid', return_value=False):
            http_request = {
                "body": {
                    "name": "any_name",
                    "email": "any_email",
                    "password": "any_password",
                    "password_confirmation": "any_password"
                }
            }

            http_response = await sut.handle(HttpRequest(**http_request))
            self.assertEqual(http_response.status_code, 400)
            self.assertEqual(http_response.body, InvalidParamError('email'))
            self.addAsyncCleanup(self.on_cleanup)

    async def test_should_call_email_validator_with_correct_email(self):
        sut_instance = make_sut()
        sut_controller = sut_instance.sut
        email_validator_stub = sut_instance.email_validator_stub
        email_validator_stub.is_valid = MagicMock()
        http_request = {
            "body": {
                "name": "any_name",
                "email": "any_email",
                "password": "any_password",
                "password_confirmation": "other_password"
            }
        }
        email_validator_stub.is_valid(http_request['body']['email'])
        await sut_controller.handle(HttpRequest(**http_request))
        email_validator_stub.is_valid.assert_called_with('any_email')

        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_call_add_account_with_correct_values(self):
        sut_instance = make_sut()
        sut = sut_instance.sut
        add_account_stub = sut_instance.add_account_stub
        add_account_stub.add = AsyncMock()
        http_request = {
            "body": {
                "name": "valid_name",
                "email": "valid_email",
                "password": "valid_password",
                "password_confirmation": "valid_password"
            }
        }
        await add_account_stub.add(AddAccountModel(name=http_request['body']['name'],
                                                   email=http_request['body']['email'],
                                                   password=http_request['body']['password']))
        await sut.handle(HttpRequest(**http_request))
        add_account_stub.add.assert_called_with(AddAccountModel(name="valid_name",
                                                                     email="valid_email",
                                                                     password="valid_password"))

    async def test_should_return_500_if_email_validator_throws(self):
        sut_instance = make_sut()
        sut = sut_instance.sut

        email_validator_stub = sut_instance.email_validator_stub

        def raise_exception():
            raise ServerError()

        with patch.object(email_validator_stub.__class__, 'is_valid', side_effect=raise_exception):
            http_request = {
                "body": {
                    "name": "valid_name",
                    "email": "valid_email",
                    "password": "valid_password",
                    "password_confirmation": "valid_password"
                }
            }

            http_response = await sut.handle(HttpRequest(**http_request))
            self.assertEqual(http_response.status_code, 500)
            self.assertEqual(http_response.body, ServerError())

            self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_500_if_add_account_throws(self):
        sut_instance = make_sut()
        sut = sut_instance.sut

        add_account_stub = sut_instance.add_account_stub

        def raise_exception():
            raise ServerError()

        with patch.object(add_account_stub.__class__, 'add', side_effect=raise_exception):
            http_request = {
                "body": {
                    "name": "valid_name",
                    "email": "valid_email",
                    "password": "valid_password",
                    "password_confirmation": "valid_password"
                }
            }

            http_response = await sut.handle(HttpRequest(**http_request))
            self.assertEqual(http_response.status_code, 500)
            self.assertEqual(http_response.body, ServerError())

            self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_200_if_data_is_provided(self):
        sut_instance = make_sut()
        sut = sut_instance.sut

        http_request = {
            "body": {
                "name": "valid_name",
                "email": "valid_email",
                "password": "valid_password",
                "password_confirmation": "valid_password"
            }
        }

        http_response = await sut.handle(HttpRequest(**http_request))
        self.assertEqual(http_response.status_code, 200)

        self.assertEqual(http_response.body, AccountModel(id="valid_id", name="valid_name", email="valid_email",
                                                          password="valid_password"))

        self.addAsyncCleanup(self.on_cleanup)

    async def on_cleanup(self):
        events.append("cleanup")


if __name__ == "__main__":
    unittest.main()
