from abc import ABC, abstractmethod
from typing import Callable, List

from models.notifications import Notification


class BaseDatabase(ABC):
    """Абстрактный класс для реляционной базы данных."""

    @abstractmethod
    def get_users_emails(self, user_id_list: List[str]) -> List:
        """Запрос имени пользователя по его почте.

        Args:
            user_id_list(list): Спискок пользователей, чъя почта необходима

        Returns:
            (list): Список пар {user_id: email}
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
    def get_users_by_movie_id(self, movie_id: str) -> List[str]:
        """Запрос для получения списка пользователей подписанных на фильм.

        Args:
            movie_id(str): идентификатор фильма.

        Returns:
            users(List[str]): Список пользователей подписанных на фильм.
        """
