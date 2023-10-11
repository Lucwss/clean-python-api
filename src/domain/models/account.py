from src.presentation.protocols.interface import BaseModel


class AccountModel(BaseModel):
    id: str
    name: str
    email: str
    password: str
