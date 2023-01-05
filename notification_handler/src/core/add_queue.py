import backoff
import pika
from pika import BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError

from core.settings import get_settings

settings = get_settings()


@backoff.on_exception(backoff.expo, AMQPConnectionError)
def add_queue() -> None:
    """Добавление очереди для уведомлений в RabbitMQ."""
    credentials = pika.PlainCredentials(settings.rb_user, settings.rb_password)
    connection = BlockingConnection(
        ConnectionParameters(host=settings.rb_host, port=settings.rb_port, credentials=credentials),
    )
    channel = connection.channel()
    channel.queue_declare("Notification")
    channel.queue_declare("Generator")
    connection.close()
