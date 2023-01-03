from functools import lru_cache
from typing import Optional

from aio_pika import Connection

rabbitmq: Optional[Connection] = None


@lru_cache
def get_rabbit() -> Connection:
    """Фабрика для получения подключения к Rabbitmq.

    Returns:
        rabbitmq(Connection): Экземпляр подключения
    """
    return rabbitmq
