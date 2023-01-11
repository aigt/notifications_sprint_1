from typing import Optional

from models.orjson import OrjsonModel


class Notification(OrjsonModel):
    """Родительский класс уведомлений."""

    fields: Optional[dict]
