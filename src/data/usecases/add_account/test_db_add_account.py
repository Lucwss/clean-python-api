from unittest import IsolatedAsyncioTestCase
import unittest
from unittest.mock import AsyncMock, patch

from src.data.protocols.add_account_repository import AddAccountRepository
from src.data.protocols.encrypter import Encrypter
from src.data.usecases.add_account.db_add_account import DbAddAccount
from src.domain.models.account import AccountModel
from src.domain.usecases.add_account import AddAccountModel
from src.presentation.protocols.interface import BaseInterface


class SutTypes(BaseInterface):
    sut: DbAddAccount
    encrypter_stub: Encrypter
    add_account_repository_stub: AddAccountRepository


def make_encrypter_stub() -> Encrypter:
    class EncrypterStub(Encrypter):
        password = "hashed_password"

        async def encrypt(self, value: str) -> str:
            return self.password

    return EncrypterStub()


def make_add_account_repository_stub() -> AddAccountRepository:
    class AddAccountRepositoryStub(AddAccountRepository):
        async def add(self, account_data: AddAccountModel) -> AccountModel:
            fake_account = {
                "id": "valid_id",
                "name": "valid_name",
                "email": "valid_email",
                "password": "hashed_password"
            }
            return AccountModel(**fake_account)

    return AddAccountRepositoryStub()


def make_sut() -> SutTypes:
    encrypter_stub = make_encrypter_stub()
    add_account_repository_stub = make_add_account_repository_stub()
    sut = DbAddAccount(encrypter=encrypter_stub, add_account_repository=add_account_repository_stub)
    return SutTypes(sut=sut, encrypter_stub=encrypter_stub, add_account_repository_stub=add_account_repository_stub)


events = []


class TestDbAddAccount(IsolatedAsyncioTestCase):

    def setUp(self):
        events.append("setUp")

    async def test_should_throw_if_encrypter_throws(self):
        sut_instance = make_sut()
        sut = sut_instance.sut
        encrypter_stub = sut_instance.encrypter_stub

        with patch.object(encrypter_stub.__class__, 'encrypt') as mocked_method:
            account_data = {
                "name": "valid_name",
                "email": "valid_email",
                "password": "valid_password"
            }

            mocked_method.side_effect = Exception()

            with self.assertRaises(Exception):
                await sut.add(AddAccountModel(**account_data))

        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_throw_if_add_account_repository_throws(self):
        sut_instance = make_sut()
        sut = sut_instance.sut
        add_account_repository_stub = sut_instance.add_account_repository_stub

        with patch.object(add_account_repository_stub.__class__, 'add') as mocked_method:
            account_data = {"name": "valid_name", "email": "valid_email", "password": "valid_password"}

            mocked_method.side_effect = Exception()

            with self.assertRaises(Exception):
                await sut.add(AddAccountModel(**account_data))

        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_call_encrypter_with_correct_password(self):
        sut_instance = make_sut()
        sut = sut_instance.sut
        encrypter_stub = sut_instance.encrypter_stub
        encrypter_stub.encrypt = AsyncMock()
        encrypter_stub.encrypt.return_value = "hashed_password"

        account_data = {
            "name": "valid_name",
            "email": "valid_email",
            "password": "valid_password"
        }

        await sut.add(AddAccountModel(**account_data))
        encrypter_stub.encrypt.assert_called_with('valid_password')

        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_call_add_Account_repository_with_correct_values(self):
        sut_instance = make_sut()
        sut = sut_instance.sut
        add_account_repository_stub = sut_instance.add_account_repository_stub

        add_account_repository_stub.add = AsyncMock()

        account_data = {"name": "valid_name", "email": "valid_email", "password": "valid_password"}

        await sut.add(AddAccountModel(**account_data))

        add_account_repository_stub.add.assert_called_with(AddAccountModel(name="valid_name", email="valid_email",
                                                                           password="hashed_password"))

        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_an_account_on_success(self):
        sut = make_sut().sut
        account_data = {"name": "valid_name", "email": "valid_email", "password": "valid_password"}
        account = await sut.add(AddAccountModel(**account_data))
        self.assertEqual(account, AccountModel(id="valid_id", name="valid_name", email="valid_email",
                                               password="hashed_password"))

    async def on_cleanup(self):
        events.append("cleanup")


if __name__ == "__main__":
    unittest.main()
