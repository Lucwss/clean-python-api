from abc import ABC, abstractmethod

from .http import HttpRequest, HttpResponse


class Controller(ABC):
    @abstractmethod
    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        raise NotImplementedError()
