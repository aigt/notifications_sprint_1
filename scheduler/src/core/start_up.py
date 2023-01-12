import pika

from pika import BlockingConnection, ConnectionParameters

from core.settings import get_settings
from db.rabbit import rabbitmq


settings = get_settings()


def start_up() -> None:
    """Создание подключений на старте приложения."""
    rabbitmq.rabbitmq_con = BlockingConnection(
        ConnectionParameters(
            host=settings.rb_host,
            port=settings.rb_port,
            credentials=pika.PlainCredentials(settings.rb_user, settings.rb_password),
        ),
    )
