from src.data.protocols.add_account_repository import AddAccountRepository
from src.data.protocols.encrypter import Encrypter
from src.domain.models.account import AccountModel
from src.domain.usecases.add_account import AddAccount, AddAccountModel


class DbAddAccount(AddAccount):
    _encrypter: Encrypter
    _add_account_repository: AddAccountRepository

    def __init__(self, encrypter: Encrypter, add_account_repository: AddAccountRepository):
        self._encrypter = encrypter
        self._add_account_repository = add_account_repository

    async def add(self, account: AddAccountModel) -> AccountModel:
        encrypted_password = await self._encrypter.encrypt(account.password)
        new_account = account.model_dump()
        new_account['password'] = encrypted_password
        new_account = await self._add_account_repository.add(AddAccountModel(**new_account))
        return new_account
