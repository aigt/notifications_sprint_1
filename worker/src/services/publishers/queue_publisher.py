import json
from typing import Dict

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties

from services.publishers.publisher import Publisher


class QueuePublisher(Publisher):
    """Абстрактный сервис публикации сообщений в очередь."""

    properties = BasicProperties(
        content_type="application/json",
        content_encoding="utf-8",
        delivery_mode=2,
    )

    def __init__(
        self,
        email_rabbit_channel: BlockingChannel,
        exchange: str,
        queue: str,
    ) -> None:
        self._channel = email_rabbit_channel
        self._exchange = exchange
        self._queue = queue

    def _publish(self, message: Dict) -> None:
        """Опубликовать сообщение в очередь.

        Args:
            message (Dict): Сообщение для публикации.
        """
        body = json.dumps(
            obj=message,
            separators=(",", ":"),
            ensure_ascii=False,
        )

        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._queue,
            body=body,
            properties=self.properties,
        )
