from uuid import UUID

from pydantic import EmailStr

from models.orjson import OrjsonModel


class WelcomeFieldsModel(OrjsonModel):
    """Модель данных ожидаемых из fileds поля уведомления welcome."""

    email: EmailStr
    confirmation_url: str
    user_id: UUID
