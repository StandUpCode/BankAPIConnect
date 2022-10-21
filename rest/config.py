from pydantic import BaseSettings, Field


class RESTConfig(BaseSettings):
    JWT_SECRET = Field(..., env="JWT_SECRET")

