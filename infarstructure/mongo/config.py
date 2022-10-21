from pydantic import BaseSettings, Field


class MongoDBConfig(BaseSettings):
    MONGODB_URI = Field(..., env="MONGODB_URI")
