import backoff
import uvicorn
from aio_pika import connect_robust
from api import health
from api.v1.api import api_router
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import get_settings
from core.openapi_docs import API_DESCRIPTION, CONTACT
from db import rabbit

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


@app.on_event("startup")
@backoff.on_exception(backoff.expo, ConnectionError)
async def startup_event() -> None:
    """Функция выполняемая перед запуском приложения."""
    rabbit.rabbitmq = await connect_robust(
        host=settings.rb_host,
        port=settings.rb_port,
        login=settings.rb_user,
        password=settings.rb_password,
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Функция выполняемая перед завершением приложения."""
    await rabbit.rabbitmq.close()


app.include_router(health.router, prefix=settings.api_health, tags=["api_healthcheck"])
app.include_router(api_router, prefix=settings.api_v1_str)


def local_start() -> None:
    """Фунция для локального запуска приложения."""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,  # noqa: WPS432
    )


if __name__ == "__main__":
    local_start()
