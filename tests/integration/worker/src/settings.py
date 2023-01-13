"""Конфиг."""

from functools import lru_cache

from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    """Настройки приложения."""

    templates_dsn: PostgresDsn = Field(
        default="postgresql://app:postgres@templates_db:5432/templates",
    )

    history_dsn: PostgresDsn = Field(
        default="postgresql://app:postgres@history_db:5432/history",
    )


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()
