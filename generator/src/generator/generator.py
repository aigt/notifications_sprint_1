import logging
from typing import Any, Optional

import pyshorteners
from pydantic import ValidationError

from core.settings import get_settings
from db.base import BaseDatabase, BaseDocumentData, BaseQueue
from models.notifications import (
    NotificationFromNotifications,
    NotificationTargets,
    NotificationType,
    TaskForWorker,
)
from models.welcome_model import WelcomeFieldsModel
from services.auth_data_client import AuthDataClient

settings = get_settings()
logger = logging.getLogger(__name__)


class Generator:
    """Класс генерирующий уведомления для воркера получаемые из очереди."""

    def __init__(
        self,
        queue: BaseQueue,
        ugc_base: BaseDocumentData,
        users_base: BaseDatabase,
        auth_data_client: AuthDataClient,
    ):
        self.queue = queue
        self.ugc_base = ugc_base
        self.users_base = users_base
        self.auth_data_client = auth_data_client

    def create_data_for_worker(
        self,
        notification: NotificationFromNotifications,
    ) -> None:
        """Обработка уведомления для передачи в очередь воркера.

        Args:
            notification(NotificationFromNotifications): Уведомление из очереди.
        """
        if notification.type == NotificationType.welcome:
            if self.create_welcome(notification):
                self.queue.send(
                    settings.rb_transfer_queue,
                    self.create_welcome(notification),
                )
        elif notification.type == NotificationType.show_subs:
            self.create_new_series(notification)

        elif notification.type == NotificationType.info:
            self.create_info(notification)

    def create_new_series(self, notification: NotificationFromNotifications) -> None:
        """Создание уведомлений о выходе новой серии.

        Args:
            notification(NotificationFromNotifications): запрос из очереди.

        Returns:
            None
        """
        movie_id = notification.fields.get("movie_id")
        if movie_id is None:
            return None
        users = self.ugc_base.get_users_by_movie_id(movie_id)
        if users is None or len(users) == 0:
            return None
        emails = self.users_base.get_users_emails(users)

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

    def create_welcome(
        self,
        notification: NotificationFromNotifications,
    ) -> Optional[TaskForWorker]:
        """Подготовка задачи для welcome сообщения.

        Args:
            notification(NotificationFromNotifications): Уведомление

        Returns:
            TaskForWorker: задача для отправки в очередь к воркеру.
        """
        try:
            welcome = WelcomeFieldsModel(**notification.fields)
        except ValidationError as err:
            logger.info(f"{err}\n incorrect field data")
            return None

        tini_url = self.create_tiny_url(welcome.confirmation_url)
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
        return pyshorteners.Shortener().clckru.short(url)

    def create_info(self, notification: NotificationFromNotifications) -> None:
        """Подготовка задач типа info для передачи воркеру.

        Args:
            notification(NotificationFromNotifications): уведомление
        """
        for user in self.auth_data_client.users_data():
            task = TaskForWorker(
                template=notification.type,
                user_id=user.user_id,
                targets=[NotificationTargets.email],
                email=user.email,
                fields=notification.fields,
            )
            self.queue.send(
                settings.rb_transfer_queue,
                task,
            )
