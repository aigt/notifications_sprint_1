from pydantic import EmailStr
from services.orjson import OrjsonModel


class NotifyRequest(OrjsonModel):
    """Модель запроса для отправки Welcome письма."""

    user_id: str
    email: EmailStr
