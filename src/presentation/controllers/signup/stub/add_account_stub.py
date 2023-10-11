from src.domain.models.account import AccountModel
from src.domain.usecases.add_account import AddAccount, AddAccountModel


class AddAccountStubStub(AddAccount):
    async def add(self, account: AddAccountModel) -> AccountModel:
        fake_account = {
            "id": "valid_id",
            "name": "valid_name",
            "email": "valid_email",
            "password": "valid_password"
        }

        return AccountModel(**fake_account)
