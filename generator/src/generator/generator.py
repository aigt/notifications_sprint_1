import logging
from typing import Any, Optional

import pyshorteners
from pydantic import ValidationError

from core.settings import get_settings
from db.base import BaseDatabase, BaseDocumentData, BaseQueue
from models.notifications import (
    NotificationFromNotifications,
    NotificationType,
    TaskForWorker,
)
from models.welcome_model import WelcomeFieldsModel

settings = get_settings()
logger = logging.getLogger(__name__)


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
            if self.create_welcome(notification):
                self.queue.send(
                    settings.rb_transfer_queue,
                    self.create_welcome(notification),
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
            targets=["email"],
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
