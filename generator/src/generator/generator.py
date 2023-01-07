from db.base import BaseDatabase, BaseDocumentData, BaseQueue
from models.notifications import NotificationFromNotifications, NotificationType


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
            self.create_welcome(notification)

    def create_welcome(self, notification: NotificationFromNotifications) -> None:
        """Подготовка уведомления для welcome сообщения.

        Args:
            notification(NotificationFromNotifications): Уведомление
        """
