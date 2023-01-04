from functools import lru_cache
from typing import Callable, Optional

from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from core.settings import get_settings

rabbitmq_con: Optional[BlockingConnection] = None

settings = get_settings()


@lru_cache
def get_rabbit_con() -> BlockingConnection:
    """Фабрика для получения соединения с rabbitmq.

    Returns:
        rabbitmq_con(BlockingConnection): соединение с rabbitmq
    """
    return rabbitmq_con


class Rabbit:
    """Класс для работы с RabbitMQ."""

    def __init__(self, connect: BlockingConnection):
        self._con = connect
        self._channel = self._con.channel()

    def start_consume(self, callback: Callable) -> None:
        """Запуск считывания поступающих данных.

        Args:
            callback(Callable): Функция обработчик входящих данных
        """
        self._channel.basic_consume(settings.rb_queue_name, callback)
        self._channel.start_consuming()


def callback(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes,
) -> None:
    """Обработка поступающих данных.

    Args:
        ch(BlockingChannel): Rabbitmq канал
        method(Basic.Deliver): Доставщик
        properties(BasicProperties): Свойства
        body(bytes): Тело данных из очереди
    """
    ch.basic_ack(delivery_tag=method.delivery_tag)
