from typing import Any
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


settings = Config()


app_configs: dict[str, Any] = {
    "title": settings.APP_NAME,
    "version": settings.APP_VERSION
}