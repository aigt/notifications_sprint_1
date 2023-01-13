import json
import logging

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties


class EmailPublisher:
    """Сервис публикации писем в очередь."""

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

    def publish(self, email: str, email_content: str) -> None:
        """Добавить в очередь на отправку письмо.

        Args:
            email (str): Email, на который отправить письмо.
            email_content (str): Содержимое письма.
        """
        message = {"email": email, "content": email_content}
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

        logging.info("Worker EmailPublisher published email message")
