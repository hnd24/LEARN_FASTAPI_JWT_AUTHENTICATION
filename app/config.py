from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url_postgresql: str | None = None
    database_url_sqlite: str | None = None

    model_config = SettingsConfigDict(
        env_file = str(ROOT / ".env"),
        env_file_encoding = "utf-8",
    )

settings = Settings()
