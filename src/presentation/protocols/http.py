from typing import Any

from .interface import BaseInterface


class HttpResponse(BaseInterface):
    status_code: int
    body: Any


class HttpRequest(BaseInterface):
    body: Any
