from pydantic import BaseSettings, Field


class SCBConfig(BaseSettings):
    SCB_API_KEY: str = Field(..., env="SCB_API_KEY")
    SCB_API_SECRET: str = Field(..., env="SCB_API_SECRET")
