from fastapi import APIRouter, Depends
from starlette import status

from api.v1.add_notification.services import (
    AddNotificationService,
    get_add_notification_service,
)
from models.model_for_queue import Notification
from models.response_models import AddNotificationResponse

add_notification = APIRouter()


@add_notification.post(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=AddNotificationResponse,
)
async def new_series(
    notify_data: Notification,
    service: AddNotificationService = Depends(get_add_notification_service),
) -> AddNotificationResponse:
    """Запросить отправку уведомлений.

    Args:
        notify_data (Notification): Данные для генерации рассылки
        service (AddNotificationService): Сервис. По умолчанию Depends(get_add_notification_service).

    Returns:
        AddNotificationResponse: Модель ответа.
    """
    await service.send_notification_in_queue(notify_data)
    return AddNotificationResponse()
