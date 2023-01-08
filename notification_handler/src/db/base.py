from abc import ABC, abstractmethod
from typing import Callable

from models.notification import Notification


class BaseDatabase(ABC):
    """Абстрактный класс для реляционной базы данных."""

    @abstractmethod
    def add_personal_notification(self, notification: Notification) -> None:
        """Добавление данных в таблицу personal.

        Args:
            notification(Notification): Данные для добавления в таблицу
        """
        raise NotImplementedError()

    @abstractmethod
    def add_mass_notification(self, notification: Notification) -> None:
        """Добавление данных в таблицу mass.

        Args:
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
