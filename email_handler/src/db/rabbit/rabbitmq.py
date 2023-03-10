from functools import lru_cache
from typing import Callable, Optional

from pika import BlockingConnection

from core.config import get_settings
from db.base import BaseQueue

rabbitmq_con: Optional[BlockingConnection] = None

settings = get_settings()


@lru_cache
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
        self._channel.basic_consume(queue="email", on_message_callback=callback, auto_ack=False)
        self._channel.start_consuming()


@lru_cache()
def get_rabbit() -> Rabbit:
    """Фабрика для получения экземпляра класса Rabbit.

    Returns:
        Rabbit(Rabbit): экземпляр для работы с RabbitMQ
    """
    return Rabbit(get_rabbit_con())
