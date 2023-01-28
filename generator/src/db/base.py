from abc import ABC, abstractmethod
from typing import Callable, List

from models.notifications import Notification


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
