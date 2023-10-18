from unittest import IsolatedAsyncioTestCase
import unittest
from unittest.mock import patch, AsyncMock

from src.data.protocols.encrypter import Encrypter
from src.infra.criptography.bcrypt_adapter import BcryptAdapter
from src.presentation.protocols.interface import BaseInterface


class SutTypes(BaseInterface):
    sut: Encrypter


def make_sut() -> SutTypes:
    sut = BcryptAdapter()
    return SutTypes(sut=sut)


events = []


class TestBcryptAdapter(IsolatedAsyncioTestCase):
    def setUp(self):
        events.append("setUp")

    async def test_should_call_bcrypt_with_correct_value(self):
        sut = make_sut().sut
        sut.encrypt = AsyncMock()

        await sut.encrypt('any_value')

        sut.encrypt.assert_called_with('any_value')

        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_return_a_hash_on_success(self):
        sut = make_sut().sut

        with patch.object(sut.__class__, 'encrypt', return_value="hash"):
            hashed = await sut.encrypt('any_value')
            self.assertEqual(hashed, 'hash')

        self.addAsyncCleanup(self.on_cleanup)

    async def test_should_throw_an_error_when_thrown(self):
        sut = make_sut().sut

        with patch.object(sut.__class__, 'encrypt') as mocked_value:
            mocked_value.side_effect = Exception()

            with self.assertRaises(Exception):
                await sut.encrypt('any_value')

        self.addAsyncCleanup(self.on_cleanup)

    async def on_cleanup(self):
        events.append("cleanup")


if __name__ == "__main__":
    unittest.main()
