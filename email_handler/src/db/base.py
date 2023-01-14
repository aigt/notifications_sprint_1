from abc import ABC, abstractmethod
from typing import Callable


class BaseQueue(ABC):
    """Абстрактный класс для работы с очередью."""

    @abstractmethod
    def start_consume(self, callback: Callable) -> None:
        """Запуск считывания поступающих данных.

        Args:
            callback(Callable): Функция обработчик входящих данных
        """
