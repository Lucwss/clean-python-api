from typing import Any

from src.presentation.errors.server_error import ServerError
from src.presentation.protocols.http import HttpResponse


def bad_request(error: Exception) -> HttpResponse:
    return HttpResponse(status_code=400, body=error)


def server_error() -> HttpResponse:
    return HttpResponse(status_code=500, body=ServerError())


def ok(body: Any) -> HttpResponse:
    return HttpResponse(status_code=200, body=body)
