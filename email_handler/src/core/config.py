"""Конфигурация"""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки приложения."""

    rb_host: str = Field("localhost")
    rb_port: int = Field(5672)
    rb_user: str = Field("user")
    rb_password: str = Field("pass")
    rb_receiving_queue: str = Field("email")
    rb_transfer_queue: str = Field("Generator")

    # sendgrid_api_key: str = Field(..., env='SENDGRID_API_KEY')
    sendgrid_api_key: str = 'SENDGRID_API_KEY=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'


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """

    return Settings()
