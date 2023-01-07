from aio_pika import Connection

from core.config import get_settings

settings = get_settings()


class BaseService:
    """Родительский сервис отправки уведомлений."""

    queue_name = settings.rb_queue_name

    def __init__(self, queue: Connection):
        self.queue = queue
