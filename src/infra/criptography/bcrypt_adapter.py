from src.data.protocols.encrypter import Encrypter
from passlib.context import CryptContext


class BcryptAdapter(Encrypter):
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def encrypt(self, value: str) -> str:
        return self._pwd_context.hash(value)
