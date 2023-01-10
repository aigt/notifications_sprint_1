from typing import Any, Optional

from pydantic import EmailStr
from transform import OrjsonModel


class NotificationEmail(OrjsonModel):
    """Модель уведомления для отправки"""

    email: Optional[EmailStr]
    content: Optional[Any]
