"""Конфиг."""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки приложения."""

    # Настройки Rabbitmq
    rb_host: str = Field("localhost")
    rb_port: int = Field(5672)
    rb_user: str = Field("user")
    rb_password: str = Field("pass")
    rb_receiving_queue: str = Field("generator")
    rb_exchange: str = Field("notifications")
    rb_transfer_queue: str = Field("worker")

    # Настройки MongoDB
    mongo_dsn = Field("mongodb://localhost:27017")
    mongo_db = Field("ugc_movies")

    # Настройки gRPC сервера
    auth_host: str = Field("[::]:5001")


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()
