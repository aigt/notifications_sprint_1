from api.v1.welcome_notification.services import WelcomeService, get_welcome_service
from fastapi import APIRouter, Depends
from models.welcome_models import WelcomeNotifyRequest, WelcomeNotifyResponse
from starlette import status

welcome_router = APIRouter()


@welcome_router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=WelcomeNotifyResponse,
)
async def welcome(
    notify_data: WelcomeNotifyRequest,
    service: WelcomeService = Depends(get_welcome_service),
) -> WelcomeNotifyResponse:
    """Добавить закладку пользователю.

    Args:
        notify_data (WelcomeNotifyRequest): Данные пользователя которому будут отправлено Welcome уведомление
        service (WelcomeService): Сервис. По умолчанию Depends(get_welcome_service).

    Returns:
        WelcomeNotifyResponse: Модель ответа.
    """
    await service.add_welcome_notification_in_queue(notify_data)
    return WelcomeNotifyResponse()
