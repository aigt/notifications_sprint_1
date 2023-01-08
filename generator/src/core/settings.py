"""Конфиг."""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки приложения."""

    # Настройки Postgres User Data
    postgres_db: str = Field("users")
    postgres_user: str = Field("app")
    postgres_password: str = Field("postgres")
    postgres_host: str = Field("localhost")
    postgres_port: int = Field(5432)

    # Настройки Rabbitmq
    rb_host: str = Field("localhost")
    rb_port: int = Field(5672)
    rb_user: str = Field("user")
    rb_password: str = Field("pass")
    rb_receiving_queue: str = Field("generator")
    rb_transfer_queue: str = Field("worker")

    # Настройки MongoDB
    mongo_dsn = Field(default="mongodb://localhost:27017")
    mongo_db = Field(default="ugc_movies")


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()
