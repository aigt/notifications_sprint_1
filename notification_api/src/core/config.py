"""Конфиг."""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки приложения."""

    # Название проекта. Используется в Swagger-документации
    project_name: str = Field("movies")
    api_version: str = "1.0.0"

    api_v1_str: str = "/api/v1"
    api_health: str = "/api/health"
    api_docs_url: str = "/api/openapi"
    openapi_url: str = "/api/openapi.json"

    # Настройки пагинации
    max_page_size: int = Field(50)
    default_page_size: int = Field(5)


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()
