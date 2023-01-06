from typing import Dict

from pika.credentials import PlainCredentials

from brokers.rabbit import RabbitMQ
from core.config import Settings
from services.subscriber import Subscriber
from worker_app import WorkerApp
from workers.email import EmailWorker
from workers.history import HistoryWorker
from workers.worker import TargetWorkerName, Worker


def build() -> WorkerApp:
    """Собрать приложение.

    Returns:
        WorkerApp: Класс-приложение.
    """
    settings = Settings()

    credentials = PlainCredentials(
        username=settings.rb_user,
        password=settings.rb_password,
        erase_on_connect=False,
    )
    rabbit = RabbitMQ(
        host=settings.rb_host,
        port=settings.rb_port,
        credentials=credentials,
        max_tries_to_connect=settings.rb_max_tries_to_connect,
        connect_retry_period=settings.rb_connect_retry_period,
    )
    rabbit.connect()
    rabbit_connection = rabbit.connection

    email_worker_channel = rabbit_connection.channel()
    email_worker_channel.exchange_declare(
        exchange=settings.rb_email_exchange_name,
        durable=True,
    )
    email_worker_channel.queue_declare(
        queue=settings.rb_email_queue_name,
        durable=True,
    )

    subscriber_channel = rabbit_connection.channel()
    subscriber_channel.queue_declare(
        queue=settings.rb_worker_queue_name,
        durable=True,
    )

    email_worker = EmailWorker(
        email_rabbit_channel=email_worker_channel,
        exchange=settings.rb_email_exchange_name,
        queue=settings.rb_email_queue_name,
    )
    workers: Dict[TargetWorkerName, Worker] = {
        "email": email_worker,
    }

    # history_worker выполняется для всех сообщений, поэтому он устанавливается
    # отдельно от указываемых в сообщениях
    history_worker = HistoryWorker()

    subscriber = Subscriber(
        workers=workers,
        history_worker=history_worker,
        subscriber_channel=subscriber_channel,
        subscriber_queue_name=settings.rb_worker_queue_name,
    )

    return WorkerApp(subscriber=subscriber)
