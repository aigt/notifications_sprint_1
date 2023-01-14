import backoff
import pika
from pika import BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError

from core.config import get_settings
from db.rabbit import rabbitmq

settings = get_settings()


@backoff.on_exception(backoff.expo, AMQPConnectionError)
def start_up() -> None:
    """Создание подключений на старте приложения."""
    rabbitmq.rabbitmq_con = BlockingConnection(
        ConnectionParameters(
            host=settings.rb_host,
            port=settings.rb_port,
            credentials=pika.PlainCredentials(settings.rb_user, settings.rb_password),
        ),
    )


start_up()
