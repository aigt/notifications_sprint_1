import enum
from typing import Any, Optional

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
    email: Optional[EmailStr]
    periodic: bool


class Notification(OrjsonModel):
    """Родительский класс уведомлений."""


class NotificationFromNotifications(Notification):
    """Модель уведомления получаемая из очереди от обработчика уведомлений."""

    meta: Meta
    type: NotificationType
    custom_template: Optional[Any]
    fields: Optional[dict]


class NotificationForWorker(Notification):
    """Модель уведомления для добавления в очередь к воркеру."""
