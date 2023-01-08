from abc import ABC, abstractmethod
from typing import Callable

from models.notification import Notification


class BaseDatabase(ABC):
    """Абстрактный класс для реляционной базы данных."""

    @abstractmethod
    def add_notification(self, table: str, notification: Notification) -> None:
        """Добавление данных в таблицу info.

        Args:
            table(str): Имя таблицы
            notification(Notification): Данные для добавления в таблицу
        """
        raise NotImplementedError()


class BaseQueue(ABC):
    """Абстрактный класс для работы с очередью."""

    @abstractmethod
    def start_consume(self, callback: Callable) -> None:
        """Запуск считывания поступающих данных.

        Args:
            callback(Callable): Функция обработчик входящих данных
        """

    @abstractmethod
    def send(self, queue: str, notification: Notification) -> None:
        """Отправка данных в очередь.

        Args:
            queue(str): Имя очереди
            notification(Notification): Данные уведомления
        """
