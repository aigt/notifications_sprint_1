from typing import Any, Literal, Optional

from pydantic import EmailStr

from services.orjson import OrjsonModel


class Meta(OrjsonModel):
    """Модель мета данных для модели Notification."""

    urgency: Literal["immediate", "usual"]
    scale: Literal["bulk", "individual"]
    email: Optional[EmailStr]
    periodic: bool


class Notification(OrjsonModel):
    """Модель уведомления для добавления в очередь."""

    meta: Meta
    type: Literal["show_subs", "info", "welcome"]
    custom_template: Optional[Any]
    fields: Optional[dict]
