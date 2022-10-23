
from pydantic import BaseSettings, Field


class RESTConfig(BaseSettings):
    JWT_SECRET:str = Field(..., env="JWT_SECRET")

