import backoff
import pika
import psycopg
from db.postgres import postgres
from db.rabbit import rabbitmq
from pika import BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError

from core.settings import get_settings

settings = get_settings()


@backoff.on_exception(backoff.expo, (psycopg.OperationalError, AMQPConnectionError))
def start_up() -> None:
    """Создание подключений на старте приложения."""
    postgres.postgres_con = psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
    )
    rabbitmq.rabbitmq_con = BlockingConnection(
        ConnectionParameters(
            host=settings.rb_host,
            port=settings.rb_port,
            credentials=pika.PlainCredentials(settings.rb_user, settings.rb_password),
        ),
    )


start_up()
