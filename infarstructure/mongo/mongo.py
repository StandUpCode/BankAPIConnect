import motor.motor_asyncio

from .config import MongoDBConfig


class MongoDB:

    def __init__(self, config: MongoDBConfig):
        self.DatabaseName = None
        uri = config.MONGODB_URI
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)

    def getDB(self, DatabaseName: str):
        return self.client[DatabaseName]
