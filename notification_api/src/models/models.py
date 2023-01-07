from pydantic import Field

from core.responses import NOTIFICATION_ADDED
from services.orjson import OrjsonModel


class AddNotificationResponse(OrjsonModel):
    """Модель для ответа при успешном добавлении уведомления в очередь."""

    message: str = Field(NOTIFICATION_ADDED)
