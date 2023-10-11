from src.domain.usecases.add_account import AddAccount, AddAccountModel
from src.presentation.errors.invalid_param_error import InvalidParamError
from src.presentation.errors.missing_param_error import MissingParamError
from src.presentation.helpers.http_helper import bad_request, server_error, ok
from src.presentation.protocols.controller import Controller
from src.presentation.protocols.email_validator import EmailValidator
from src.presentation.protocols.http import HttpRequest, HttpResponse


class SignUpController(Controller):
    def __init__(self, email_validator: EmailValidator, add_account: AddAccount):
        self.email_validator = email_validator
        self.add_account = add_account

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            required_fields: list[str] = ['name', 'email', 'password', 'password_confirmation']

            for field in required_fields:
                if field not in http_request.body.keys():
                    return bad_request(MissingParamError(field))

            body = http_request.body

            if body['password'] != body['password_confirmation']:
                return bad_request(InvalidParamError('password_confirmation'))

            is_valid = self.email_validator.is_valid(body['email'])

            if not is_valid:
                return bad_request(InvalidParamError('email'))

            account = {"email": body['email'], "password": body['password'], "name": body['name']}

            account = await self.add_account.add(AddAccountModel(**account))

            return ok(account)
        except Exception as ex:
            print(ex)
            return server_error()

