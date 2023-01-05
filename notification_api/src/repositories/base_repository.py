from abc import ABC, abstractmethod

from aio_pika import Connection

from models.model_for_queue import Notification


class BaseRepository(ABC):
    """Абстрактный класс репозитория брокера сообщений."""

    queue_name = "Notification"

    def __init__(self, queue: Connection):
        self.queue = queue

    @abstractmethod
    async def add_in_queue(self, notify: Notification) -> None:
        """Добавление данных в очередь.

        Args:
            notify(Notification): Данные передаваемые в очередь
        """
        raise NotImplementedError
