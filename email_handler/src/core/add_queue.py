import backoff
import pika
from pika.exceptions import AMQPConnectionError

from core.config import get_settings

config = get_settings()


@backoff.on_exception(backoff.expo, AMQPConnectionError)
def add_queue() -> None:
    """Добавление очереди для уведомлений в RabbitMQ."""

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=config.rb_host,
            port=config.rb_port,
            credentials=pika.PlainCredentials(config.rb_user,
                                              config.rb_password),
        ),
    )
    channel = connection.channel()

    channel.queue_declare(queue='email', durable=True)
    connection.close()
