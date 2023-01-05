from jinja2 import BaseLoader, Environment
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties

from services import template
from workers.worker import Worker, WorkerMessage


class EmailWorker(Worker):
    """Воркер обрабатывающий Email."""

    def __init__(
        self,
        email_rabbit_channel: BlockingChannel,
        exchange: str,
        queue: str,
    ) -> None:
        self._channel = email_rabbit_channel
        self._exchange = exchange
        self._queue = queue

    def run(self, message: WorkerMessage) -> None:
        """Обработать сообщение.

        Args:
            message (WorkerMessage): Сообщение для обработки.
        """
        rendered_email = self.render_email(message)
        self.publish_email(rendered_email)

    def render_email(self, message: WorkerMessage) -> str:
        """Рендерить Email.

        Args:
            message (WorkerMessage): Сообщение для обработки.

        Returns:
            str: Письмо.
        """
        str_template = template.get(message.template)
        jinja_template = Environment(loader=BaseLoader(), autoescape=True).from_string(
            str_template,
        )
        return jinja_template.render(**message.fields)  # type: ignore

    def publish_email(self, email: str) -> None:
        """Добавить в очередь на отправку письмо.

        Args:
            email (str): Письмо.
        """
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._queue,
            body=email,
            properties=BasicProperties(content_type="text/plain"),
        )
