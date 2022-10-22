from pydantic import BaseSettings, Field


class MongoDBConfig(BaseSettings):
    MONGODB_URI:str = Field(..., env="MONGODB_URI")
