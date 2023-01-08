from core.settings import get_settings
from db.base import BaseDatabase, BaseQueue
from models.notification import Notification, NotificationScale, NotificationUrgency

settings = get_settings()


class NotificationHandler:
    """Сортировщик данных получаемых из очереди."""

    def __init__(
        self,
        db: BaseDatabase,
        queue: BaseQueue,
    ):
        self.db = db
        self.queue = queue

    def sort(self, notification: Notification) -> None:
        """Определение направления для уведомления.

        Если уведомление срочное, отправка идет сразу в очередь к генератору.

        Args:
            notification(Notification): Уведомление
        """
        if notification.meta.urgency == NotificationUrgency.immediate:
            self.queue.send(settings.rb_transfer_queue, notification)

        elif notification.meta.scale == NotificationScale.bulk:
            self.db.add_notification(notification=notification, table=settings.t_bulk)

        elif notification.meta.scale == NotificationScale.individual:
            self.db.add_notification(
                notification=notification,
                table=settings.t_individual,
            )
