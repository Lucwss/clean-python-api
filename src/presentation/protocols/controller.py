from .http import HttpRequest, HttpResponse
from abc import ABC, abstractmethod


class Controller(ABC):
    @abstractmethod
    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        raise NotImplementedError()
