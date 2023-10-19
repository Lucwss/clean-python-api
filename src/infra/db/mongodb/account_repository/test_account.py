import unittest
from unittest import IsolatedAsyncioTestCase

from src.data.protocols.add_account_repository import AddAccountRepository
from src.domain.usecases.add_account import AddAccountModel
from src.infra.db.mongodb.account_repository.account import AccountMongoRepository
from src.presentation.protocols.interface import BaseInterface


class SutTypes(BaseInterface):
    sut: AddAccountRepository


def make_sut() -> SutTypes:
    sut = AccountMongoRepository()
    return SutTypes(sut=sut)


events = []


class TestAccountMongoRepository(IsolatedAsyncioTestCase):
    def setUp(self):
        events.append("setUp")

    async def test_should_return_an_account_on_success(self):

        sut = make_sut().sut
        account = await sut.add(AddAccountModel(
            name="any_name",
            email="any_email@email.com",
            password="any_password"
        ))

        self.assertTrue(account)
        self.assertTrue(account.id)
        self.assertEqual(account.name, 'any_name')
        self.assertEqual(account.email, 'any_email@email.com')
        self.assertEqual(account.password, 'any_password')

        self.addAsyncCleanup(self.on_cleanup)

    async def on_cleanup(self):
        events.append("cleanup")


if __name__ == '__main__':
    unittest.main()
