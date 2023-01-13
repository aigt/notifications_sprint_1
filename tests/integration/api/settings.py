"""Конфиг."""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки приложения."""

    container: str = Field("integration")

    url: str = Field("http://localhost:8000/api/v1")

    # Настройки Rabbitmq
    rb_host: str = Field("localhost")
    rb_port: int = Field(5672)
    rb_user: str = Field("user")
    rb_password: str = Field("pass")
    rb_queue: str = Field("notifications")
    rb_exchange: str = Field("notifications")

    # Настройки MongoDB
    mongo_dsn = Field("mongodb://localhost:27017")
    mongo_db = Field("ugc_movies")

    # Настройки Postgres
    postgres_user: str = Field("app")
    postgres_password: str = Field("postgres")
    postgres_host: str = Field("localhost")
    postgres_port: int = Field(5432)

    # Postgres Базы
    users_db: str = Field("users")


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()
