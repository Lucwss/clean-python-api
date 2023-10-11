from src.domain.models.account import AccountModel
from src.presentation.protocols.interface import BaseInterface
from abc import ABC, abstractmethod


class AddAccountModel(BaseInterface):
    name: str
    email: str
    password: str


class AddAccount(ABC):
    @abstractmethod
    async def add(self, account: AddAccountModel) -> AccountModel:
        raise NotImplementedError()
