from typing import Callable, Optional

from db.base import BaseQueue
from models.notifications import NotificationForWorker
from pika import BlockingConnection

from core.settings import get_settings

rabbitmq_con: Optional[BlockingConnection] = None

settings = get_settings()


def get_rabbit_con() -> BlockingConnection:
    """Фабрика для получения соединения с rabbitmq.

    Returns:
        rabbitmq_con(BlockingConnection): соединение с rabbitmq
    """
    return rabbitmq_con


class Rabbit(BaseQueue):
    """Класс для работы с RabbitMQ."""

    def __init__(self, connect: BlockingConnection):
        self._con = connect
        self._channel = self._con.channel()

    def start_consume(self, callback: Callable) -> None:
        """Запуск считывания поступающих данных.

        Args:
            callback(Callable): Функция обработчик входящих данных
        """
        self._channel.basic_consume(settings.rb_receiving_queue, callback)
        self._channel.start_consuming()

    def send(self, queue: str, notification: NotificationForWorker) -> None:
        """Отправление данных в очередь.

        Args:
            queue(str): Имя очереди
            notification(NotificationForWorker): данные для отправки
        """
        self._channel.basic_publish(
            exchange="",
            routing_key=settings.rb_transfer_queue,
            body=notification.json(),
        )


def get_rabbit() -> Rabbit:
    """Фабрика для получения экземпляра класса Rabbit.

    Returns:
        Rabbit(Rabbit): экземпляр для работы с RabbitMQ
    """
    return Rabbit(get_rabbit_con())
