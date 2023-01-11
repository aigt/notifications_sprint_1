"""Конфигурация."""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки приложения."""

    rb_host: str = Field("localhost")
    rb_port: int = Field(5672)
    rb_user: str = Field("user")
    rb_password: str = Field("pass")
    rb_receiving_queue: str = Field("email")
    rb_exchange: str = Field("notifications")

    sendgrid_api_key: str = Field(..., env="SENDGRID_API_KEY")
    email_from: str = "a1exitt@yandex.ru"


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()
