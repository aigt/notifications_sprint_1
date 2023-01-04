from functools import lru_cache
from typing import Optional

from pika import BlockingConnection

rabbitmq_con: Optional[BlockingConnection] = None


@lru_cache
def get_rabbit_con() -> BlockingConnection:
    """Фабрика для получения соединения с rabbitmq.

    Returns:
        rabbitmq_con(BlockingConnection): соединение с rabbitmq
    """
    return rabbitmq_con
