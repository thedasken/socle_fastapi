from typing import Any
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import Environment


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class Config(CustomBaseSettings):
    APP_NAME: str
    APP_VERSION: str
    ENVIRONMENT: Environment

    # Database
    DATABASE_ASYNC_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 16
    DATABASE_POOL_TTL: int = 60 * 20  # 20 minutes
    DATABASE_POOL_PRE_PING: bool = True


settings = Config()


app_configs: dict[str, Any] = {
    "title": settings.APP_NAME,
    "version": settings.APP_VERSION
}