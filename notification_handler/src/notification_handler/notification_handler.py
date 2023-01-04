from db.base import BaseDatabase, BaseQueue
from db.postgres.postgres import get_postgres
from db.rabbit.rabbitmq import get_rabbit
from models.notification import Notification, NotificationType

from core.settings import get_settings

settings = get_settings()


class NotificationHandler:
    """Сортировщик данных получаемых из очереди."""

    def __init__(
        self,
        db: BaseDatabase = get_postgres(),
        queue: BaseQueue = get_rabbit(),
    ):
        self.db = db
        self.queue = queue

    def sort(self, notification: Notification) -> None:
        """Определение направления для уведомления.

        Args:
            notification(Notification): Уведомление
        """
        if notification.type == NotificationType.welcome:
            self.welcome_handler(notification)

    def welcome_handler(self, notification: Notification) -> None:
        """Передача Welcome уведомления в очередь генератора.

        Args:
            notification(Notification): Уведомление
        """
        self.queue.send(settings.rb_transfer_queue, notification)
