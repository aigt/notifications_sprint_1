from abc import ABC, abstractmethod
from typing import Callable

from models.notifications import Notification


class BaseDatabase(ABC):
    """Абстрактный класс для реляционной базы данных."""

    @abstractmethod
    def get_user_name(self, email: str) -> None:
        """Запрос имени пользователя по его почте.

        Args:
            email(str): Почта
        """


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


class BaseDocumentData(ABC):
    """Абстрактный класс для работы с документоориентированными базами."""

    @abstractmethod
    def get_user_bookmark(self, user: str) -> str:
        """Запрос закладок пользователя по его имени.

        Args:
            user(str): Почта
        """
