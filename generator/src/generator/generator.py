from core.settings import get_settings
from db.base import BaseDatabase, BaseDocumentData, BaseQueue
from models.notifications import (
    NotificationForWorker,
    NotificationFromNotifications,
    NotificationType,
)

settings = get_settings()


class Generator:
    """Класс генерирующий уведомления для воркера получаемые из очереди."""

    def __init__(
        self,
        queue: BaseQueue,
        ugc_base: BaseDocumentData,
        users_base: BaseDatabase,
    ):
        self.queue = queue
        self.ugc_base = ugc_base
        self.users_base = users_base

    def create_data_for_worker(
        self,
        notification: NotificationFromNotifications,
    ) -> None:
        """Обработка уведомления для передачи в очередь воркера.

        Args:
            notification(NotificationFromNotifications): Уведомление из очереди.
        """
        if notification.type == NotificationType.welcome:
            self.queue.send(
                settings.rb_transfer_queue,
                self.create_welcome(notification),
            )

    @staticmethod
    def create_welcome(
        notification: NotificationFromNotifications,
    ) -> NotificationForWorker:
        """Подготовка уведомления для welcome сообщения.

        Args:
            notification(NotificationFromNotifications): Уведомление

        Returns:
            NotificationForWorker: данные для отправки в очередь к воркеру.
        """
        return NotificationForWorker(
            email=notification.meta.email,
            template=notification.type,
            fields=notification.fields,
        )
