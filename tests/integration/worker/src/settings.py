"""Конфиг."""

from functools import lru_cache

from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    """Настройки приложения."""

    # Настройки Postgres
    # templates_db: str = Field("templates")
    # templates_user: str = Field("app")
    # templates_password: str = Field("postgres")
    # templates_host: str = Field("templates_db")
    # templates_port: int = Field(5432)
    templates_dsn: PostgresDsn = Field(
        default="postgresql://app:postgres@templates_db:5432/templates",
    )


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()
