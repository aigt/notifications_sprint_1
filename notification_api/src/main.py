import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from notification_api.src.api import health

from core.config import get_settings
from core.openapi_docs import API_DESCRIPTION, CONTACT

settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    description=API_DESCRIPTION,
    version=settings.api_version,
    docs_url=settings.api_docs_url,
    contact=CONTACT,
    openapi_url=settings.openapi_url,
    default_response_class=ORJSONResponse,
)

app.include_router(health.router, prefix=settings.api_health, tags=["api_healthcheck"])


def local_start() -> None:
    """Фунция для локального запуска приложения."""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,  # noqa: WPS432
    )


if __name__ == "__main__":
    local_start()
