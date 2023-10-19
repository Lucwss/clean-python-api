from fastapi import FastAPI

from .middlewares import set_up_middlewares

app = FastAPI()

set_up_middlewares(app)
