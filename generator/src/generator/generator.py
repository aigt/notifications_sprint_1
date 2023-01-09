from typing import List

from core.settings import get_settings
from db.base import BaseDatabase, BaseDocumentData, BaseQueue
from models.notifications import (
    NotificationFromNotifications,
    NotificationType,
    TaskForWorker,
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

    def create_new_series(self, notification: NotificationFromNotifications) -> None:
        """Создание уведомлений о выходе новой серии.

        Args:
            notification(NotificationFromNotifications): запрос из очереди.
        """

    def get_users_witch_movie_subscribe(self, movie_id: str) -> None:
        """Запрос зрителей подписанных на сериал.

        Args:
            movie_id(str): идентификатор сериала.
        """

    def get_users_email(self, user_id_list: List[str]) -> None:
        """Запрос почты пользотелей.

        Args:
            user_id_list(list): Список пользователей
        """

    @staticmethod
    def create_welcome(
        notification: NotificationFromNotifications,
    ) -> TaskForWorker:
        """Подготовка задачи для welcome сообщения.

        Args:
            notification(NotificationFromNotifications): Уведомление

        Returns:
            TaskForWorker: задача для отправки в очередь к воркеру.
        """
        return TaskForWorker(
            targets=["email"],
            email=notification.fields.get("email"),
            template=notification.type,
            fields=notification.fields,
            user_id=notification.fields.get("user_id"),
        )
