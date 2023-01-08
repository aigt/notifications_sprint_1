import backoff
import pika
from pika import BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError
from settings import get_settings

settings = get_settings()


@backoff.on_exception(backoff.expo, AMQPConnectionError)
def add_queue() -> None:
    """Добавление очереди для уведомлений в RabbitMQ"""
    credentials = pika.PlainCredentials(settings.rb_user, settings.rb_password)
    connection = BlockingConnection(
        ConnectionParameters(host=settings.rb_host, port=settings.rb_port, credentials=credentials),
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=settings.rb_exchange)
    channel.queue_declare(settings.rb_transfer_queue)
    channel.queue_declare(settings.rb_receiving_queue)
    channel.queue_bind(exchange=settings.rb_exchange, queue=settings.rb_transfer_queue)
    channel.queue_bind(exchange=settings.rb_exchange, queue=settings.rb_receiving_queue)
    connection.close()


if __name__ == "__main__":
    add_queue()
