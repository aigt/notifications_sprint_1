from fastapi import APIRouter

from core.config import get_settings

welcome_router = APIRouter()
settings = get_settings()


@welcome_router.get(
    path="/",
    response_model="",
)
async def welcome() -> None:
    """Представление для отправления уведомления welcome."""
