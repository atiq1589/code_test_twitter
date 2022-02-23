import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    APP_NAME: str
    DB_CONNECTION: str
    CACHE_CONNECTION: str
    CACHE_PORTS: List[int]

    class Config:
        env_file = ".env"

settings = Settings()

