from abc import ABC, abstractmethod

from models.notification import Notification


class BaseDatabase(ABC):
    """Абстрактный класс для реляционной базы данных."""

    @abstractmethod
    def add_notification_in_info_table(self, notification: Notification) -> None:
        """Добавление данных в таблицу info.

        Args:
            notification(Notification): Данные для добавления в таблицу
        """
