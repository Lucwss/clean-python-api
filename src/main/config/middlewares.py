from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.main.middlewares.content_type import ContentTypeMiddleware


def set_up_middlewares(app: FastAPI):
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.add_middleware(ContentTypeMiddleware)
