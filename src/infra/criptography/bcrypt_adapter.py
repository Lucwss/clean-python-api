from passlib.context import CryptContext

from src.data.protocols.encrypter import Encrypter


class BcryptAdapter(Encrypter):
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def encrypt(self, value: str) -> str:
        return self._pwd_context.hash(value)
