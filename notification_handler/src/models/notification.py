import enum
from typing import Any, Optional
from uuid import UUID

from pydantic import EmailStr

from models.orjson import OrjsonModel


class NotificationUrgency(enum.Enum):
    """Типы срочности уведомления."""

    immediate = "immediate"
    usual = "usual"


class NotificationScale(enum.Enum):
    """Типы массовости уведомления."""

    bulk = "bulk"
    individual = "individual"


class NotificationType(enum.Enum):
    """Типы уведомлений."""

    show_subs = "show_subs"
    info = "info"
    welcome = "welcome"


class Meta(OrjsonModel):
    """Модель мета данных для модели Notification."""

    urgency: NotificationUrgency
    scale: NotificationScale
    periodic: bool


class Notification(OrjsonModel):
    """Модель уведомления для добавления в очередь."""

    meta: Meta
    type: NotificationType
    custom_template: Optional[Any]
    fields: Optional[dict]
    user_id: Optional[UUID]
    email: Optional[EmailStr]
