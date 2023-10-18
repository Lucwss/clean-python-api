from typing import Any

import motor.motor_asyncio
from pymongo import collection


class MongoHelper:
    def __init__(self):
        self.host = ""
        self.port = 0
        self.user = ""
        self.password = ""
        self.connection = self._connection()

    def _connection(self):
        return motor.motor_asyncio.AsyncIOMotorClient(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password
        )

    def database(self):
        return self.connection.database_name

    def get_collection(self, name: str) -> collection:
        return self.database().get_collection(name)

    def map(self, collection: Any) -> Any:
        pass
