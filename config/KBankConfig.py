from pydantic import BaseSettings, Field


class KBankConfig(BaseSettings):
    KBANK_CONSUMER_ID: str = Field(..., env="KBANK_CONSUMER_ID")
    KBANK_CONSUMER_SECRET: str = Field(..., env="KBANK_CONSUMER_SECRET")
