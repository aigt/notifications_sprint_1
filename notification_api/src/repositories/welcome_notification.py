from functools import lru_cache

import aio_pika
from aio_pika import Connection
from db.rabbit import get_rabbit
from fastapi import Depends
from models.model_for_queue import Notification
from repositories.base_repository import BaseRepository


class WelcomeRepository(BaseRepository):
    """Репозиторий для работы с Welcome уведомлениями."""

    async def add_in_queue(self, notify: Notification) -> None:
        """Добавление данных в очередь.

        Args:
            notify(Notification): Данные передаваемые в очередь
        """
        channel = await self.queue.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=notify.json().encode()),
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
