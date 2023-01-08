from functools import lru_cache

import aio_pika

from api.v1.base import BaseService
from core.config import get_settings
from db.rabbit import get_rabbit
from models.model_for_queue import Notification

settings = get_settings()


class AddNotificationService(BaseService):
    """Сервис для отправки запроса на отправку уведомлений в очередь."""

    async def send_notification_in_queue(self, notify_data: Notification) -> None:
        """Отправка данных запроса в очередь для обработчика уведомлений.

        Args:
            notify_data(Notification): Данные для форматирования запроса
        """
        channel = await self.queue.channel()
        exchange = await channel.declare_exchange(name=settings.rb_exchange)
        await exchange.publish(
            aio_pika.Message(body=notify_data.json().encode()),
            routing_key=self.queue_name,
        )


@lru_cache()
def get_add_notification_service() -> AddNotificationService:
    """Фабрика для AddNotificationService.

    Returns:
        AddNotificationService: Экземпляр сервиса.
    """
    return AddNotificationService(get_rabbit())
