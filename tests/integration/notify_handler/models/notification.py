import enum
from typing import Any, Optional

from models.orjson import OrjsonModel
from pydantic import EmailStr


class NotificationUrgency(str, enum.Enum):
    """Типы срочности уведомления."""

    immediate = "immediate"
    usual = "usual"


class NotificationScale(str, enum.Enum):
    """Типы массовости уведомления."""

    bulk = "bulk"
    individual = "individual"


class NotificationType(str, enum.Enum):
    """Типы уведомлений."""

    show_subs = "show_subs"
    info = "info"
    welcome = "welcome"


class Meta(OrjsonModel):
    """Модель мета данных для модели Notification."""

    urgency: NotificationUrgency
    scale: NotificationScale
    email: Optional[EmailStr]
    periodic: bool

    class Config:
        use_enum_values = True


class Notification(OrjsonModel):
    """Модель уведомления для добавления в очередь."""

    meta: Meta
    type: NotificationType
    custom_template: Optional[Any]
    fields: Optional[dict]

    class Config:
        use_enum_values = True