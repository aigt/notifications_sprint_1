from functools import lru_cache

from pydantic import BaseSettings, Field

DEFAULT_PG_PORT = 5432
DEFAULT_RABBIT_PORT = 5672


class Settings(BaseSettings):
    """Настройки приложения."""

    # Таблицы Postgres
    t_bulk: str = "bulk"
    t_individual: str = "individual"

    # Настройки Postgres
    postgres_db: str = Field("notifications")
    postgres_user: str = Field("app")
    postgres_password: str = Field("postgres")
    postgres_host: str = Field("localhost")
    postgres_port: int = Field(DEFAULT_PG_PORT)

    # Настройки Rabbitmq
    rb_host: str = Field("localhost")
    rb_port: int = Field(DEFAULT_RABBIT_PORT)
    rb_user: str = Field("user")
    rb_password: str = Field("pass")
    rb_receiving_queue: str = Field("generator")
    rb_transfer_queue: str = Field("generator")
    rb_exchange: str = Field("notifications")


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()
