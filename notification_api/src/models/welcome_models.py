from uuid import UUID

from pydantic import EmailStr, Field
from services.orjson import OrjsonModel

from core.responses import NOTIFICATION_ADDED


class WelcomeNotifyRequest(OrjsonModel):
    """Модель запроса для отправки Welcome письма."""

    user_id: UUID
    email: EmailStr


class WelcomeNotifyResponse(OrjsonModel):
    """Модель для ответа при запросе на отправку Welcome письма."""

    message: str = Field(NOTIFICATION_ADDED)
