import enum
from typing import Any, List, Optional
from uuid import UUID

from pydantic import EmailStr

from models.base import Notification
from models.orjson import OrjsonModel


class NotificationTargets(enum.Enum):
    """Направления для уведомления."""

    email = "email"
    sms = "sms"
    push = "push"


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


class NotificationFromNotifications(Notification):
    """Модель уведомления получаемая из очереди от обработчика уведомлений."""

    meta: Meta
    type: NotificationType
    custom_template: Optional[Any]


class TaskForWorker(Notification):
    """Модель задачи для добавления в очередь к воркеру."""

    targets: List[NotificationTargets]
    template: Optional[Any]
    user_id: Optional[UUID]
    email: EmailStr
