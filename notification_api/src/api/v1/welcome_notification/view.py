import uuid

from api.v1.welcome_notification.services import WelcomeService, get_welcome_service
from fastapi import APIRouter, Body, Depends
from models.welcome_models import WelcomeNotifyResponse
from starlette import status

from core.config import get_settings

welcome_router = APIRouter()
settings = get_settings()


@welcome_router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=WelcomeNotifyResponse,
)
async def welcome(
    service: WelcomeService = Depends(get_welcome_service),
    notify_data: dict = Body(
        example={"user_id": str(uuid.uuid4()), "email": "example@gamil.com"},
        title="Данные",
        description="Идентификатор и почта пользователя для отправки уведомления",
    ),
) -> WelcomeNotifyResponse:
    """Добавить закладку пользователю.

    Args:
        notify_data (dict): Данные пользователя которому будут отправлено Welcome уведомление
        service (WelcomeService): Сервис. По умолчанию Depends(get_welcome_service).

    Returns:
        WelcomeNotifyResponse: Модель ответа.
    """
    await service.add_welcome_notification_in_queue(notify_data)
    return WelcomeNotifyResponse()
