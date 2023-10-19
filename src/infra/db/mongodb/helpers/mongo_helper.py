from typing import Any

import motor.motor_asyncio
from pymongo import collection


class MongoHelper:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 27045
        self.user = "user-access"
        self.password = "user-pass-123"
        self.connection = self._connection()

    def _connection(self):
        return motor.motor_asyncio.AsyncIOMotorClient(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password
        )

    def disconnect(self):
        self.connection.close()

    def database(self):
        return self.connection.CleanPythonMongo

    def get_collection(self, name: str) -> collection:
        return self.database().get_collection(name)

    def mapper(self, collection: dict) -> Any:
        collection['id'] = str(collection['_id'])
        collection.pop('_id')
        return collection
