from pydantic import EmailStr, Field

from core.responses import NOTIFICATION_ADDED
from services.orjson import OrjsonModel


class WelcomeNotifyRequest(OrjsonModel):
    """Модель запроса для отправки Welcome письма."""

    user_name: str
    email: EmailStr


class WelcomeNotifyResponse(OrjsonModel):
    """Модель для ответа при запросе на отправку Welcome письма."""

    message: str = Field(NOTIFICATION_ADDED)
