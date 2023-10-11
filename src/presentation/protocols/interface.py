from pydantic import BaseModel


class BaseInterface(BaseModel):
    model_config = {'arbitrary_types_allowed': True}


class BaseModel(BaseModel):
    model_config = {'arbitrary_types_allowed': True}
