from uuid import UUID

from pydantic import EmailStr

from services.orjson import OrjsonModel


class WelcomeNotifyRequest(OrjsonModel):
    """Модель запроса для отправки Welcome письма."""

    user_id: UUID
    email: EmailStr
