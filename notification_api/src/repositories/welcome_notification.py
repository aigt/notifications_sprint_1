from functools import lru_cache

import aio_pika
import orjson
from aio_pika import Connection
from fastapi import Depends
from repositories.base_repository import BaseRepository

from db.rabbit import get_rabbit
from models.model_for_queue import Notification


class WelcomeRepository(BaseRepository):
    """Репозиторий для работы с Welcome уведомлениями."""

    async def add_in_queue(self, notify: Notification) -> None:
        """Добавление данных в очередь.

        Args:
            notify(Notification): Данные передаваемые в очередь
        """
        channel = await self.queue.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=orjson.dumps(notify.json())),
            routing_key=self.queue_name,
        )


@lru_cache
def get_welcome_repo(queue: Connection = Depends(get_rabbit)) -> WelcomeRepository:
    """Фабрика для сервиса WelcomeService.

    Args:
        queue (Connection): Соединение с брокером сообщений

    Returns:
        WelcomeRepository: Экземпляр репозитория.
    """
    return WelcomeRepository(queue)
