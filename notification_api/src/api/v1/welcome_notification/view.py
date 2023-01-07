from fastapi import APIRouter, Depends
from starlette import status

from api.v1.welcome_notification.services import WelcomeService, get_welcome_service
from models.models import AddNotificationResponse
from models.welcome_models import WelcomeNotifyRequest

welcome_router = APIRouter()


@welcome_router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=AddNotificationResponse,
)
async def welcome(
    notify_data: WelcomeNotifyRequest,
    service: WelcomeService = Depends(get_welcome_service),
) -> AddNotificationResponse:
    """Запросить отправку уведомления welcome для пользователя.

    Args:
        notify_data (WelcomeNotifyRequest): Данные пользователя которому будут отправлено Welcome уведомление
        service (WelcomeService): Сервис. По умолчанию Depends(get_welcome_service).

    Returns:
        AddNotificationResponse: Модель ответа.
    """
    await service.add_welcome_notification_in_queue(notify_data)
    return AddNotificationResponse()
