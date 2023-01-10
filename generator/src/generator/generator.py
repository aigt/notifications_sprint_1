from typing import Any

import pyshorteners

from core.settings import get_settings
from db.base import BaseDatabase, BaseDocumentData, BaseQueue
from models.notifications import (
    NotificationFromNotifications,
    NotificationTargets,
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
        elif notification.type == NotificationType.show_subs:
            self.create_new_series(notification)

    def create_new_series(self, notification: NotificationFromNotifications) -> None:
        """Создание уведомлений о выходе новой серии.

        Args:
            notification(NotificationFromNotifications): запрос из очереди.
        """
        users = self.get_users_witch_movie_subscribe(
            notification.fields.get("movie_id"),
        )
        emails = self.get_users_email(users)

        for email in emails:
            task = TaskForWorker(
                template=NotificationType.show_subs,
                user_id=email.get("user_id"),
                targets=[NotificationTargets.email],
                email=email.get("email"),
                fields=notification.fields,
            )
            self.queue.send(
                settings.rb_transfer_queue,
                task,
            )

    def get_users_witch_movie_subscribe(self, movie_id: str) -> Any:
        """Запрос зрителей подписанных на сериал.

        Args:
            movie_id(str): идентификатор сериала.

        Returns:
            (list): список пользователей с сериалом в закладках
        """
        return self.ugc_base.get_users_by_movie_id(movie_id)

    def get_users_email(self, user_id_list: List[str]) -> Any:
        """Запрос почты пользователей.

        Args:
            user_id_list(list): Список пользователей

        Returns:
            (dict):
        """
        return self.users_base.get_users_emails(user_id_list)

    def create_welcome(
        self,
        notification: NotificationFromNotifications,
    ) -> TaskForWorker:
        """Подготовка задачи для welcome сообщения.

        Args:
            notification(NotificationFromNotifications): Уведомление

        Returns:
            TaskForWorker: задача для отправки в очередь к воркеру.
        """
        tini_url = self.create_tiny_url(notification.fields.get("confirmation_url"))
        notification.fields.update({"confirmation_url": tini_url})

        return TaskForWorker(
            targets=[NotificationTargets.email],
            email=notification.fields.get("email"),
            template=notification.type,
            fields=notification.fields,
            user_id=notification.fields.get("user_id"),
        )

    @staticmethod
    def create_tiny_url(url: str) -> Any:
        """Создание короткой ссылки.

        Args:
            url(str): ссылка

        Returns:
            (str): короткая ссылка
        """
        return pyshorteners.Shortener().tinyurl.short(url)
