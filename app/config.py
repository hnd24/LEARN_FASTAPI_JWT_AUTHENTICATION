# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url_postgresql: str | None = None
    database_url_sqlite: str | None = None

    class Config:
        env_file = ".env"   # chỉ định file .env

settings = Settings()
