import unittest
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase
from src.main.config.app import app

events = []


class TestContentTypeMiddleware(IsolatedAsyncioTestCase):
    def setUp(self):
        events.append("setUp")

    async def test_should_return_default_content_type_json(self):
        @app.get('/test_content_type')
        async def test_content_type():
            return ''

        async with AsyncClient(app=app, base_url='http://0.0.0.0:8002') as ac:
            response = await ac.get('/test_content_type')

        self.assertEqual(response.headers.get('Content-Type'), 'application/json')

        self.addAsyncCleanup(self.on_cleanup)

    async def on_cleanup(self):
        events.append("cleanup")


if __name__ == "__main__":
    unittest.main()
