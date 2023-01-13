import logging
from typing import Dict

from pika.credentials import PlainCredentials

from brokers.rabbit import RabbitMQ
from core.config import Settings
from services import query_loader
from services.consumer import Consumer
from services.email_publisher import EmailPublisher
from services.history_publisher import HistoryPublisher
from services.render import Render
from services.templates_storage import TemplatesStorage
from worker_app import WorkerApp
from workers.email import EmailWorker
from workers.history import HistoryWorker
from workers.worker import Worker
from workers.worker_message import TargetWorkerName


def build() -> WorkerApp:
    """Собрать приложение.

    Returns:
        WorkerApp: Класс-приложение.
    """
    settings = Settings()

    logging.info("Setting up:")
    logging.info(
        "RabbitMQ host:port: %s:%s",  # noqa: WPS323
        settings.rb_host,
        settings.rb_port,
    )
    logging.info(
        "worker_queue_name: %s",  # noqa: WPS323
        settings.rb_worker_queue_name,
    )
    logging.info(
        "email_exchange_name: %s",  # noqa: WPS323
        settings.rb_email_exchange_name,
    )
    logging.info(
        "email_queue_name: %s",  # noqa: WPS323
        settings.rb_email_queue_name,
    )
    logging.info(
        "Templates DB host:port: %s:%s",  # noqa: WPS323
        settings.tdb_dsn.host,
        settings.tdb_dsn.port,
    )

    templates_query = query_loader.load_sql(settings.tdb_template_sql_query_file)

    templates_storage = TemplatesStorage(
        coninfo=settings.tdb_dsn,
        query=templates_query,
    )

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
    email_worker_channel.queue_bind(
        queue=settings.rb_email_queue_name,
        exchange=settings.rb_email_exchange_name,
    )

    subscriber_channel = rabbit_connection.channel()
    subscriber_channel.queue_declare(
        queue=settings.rb_worker_queue_name,
        durable=True,
    )

    messages_render = Render(
        templates_storage=templates_storage,
    )

    email_publisher = EmailPublisher(
        email_rabbit_channel=email_worker_channel,
        exchange=settings.rb_email_exchange_name,
        queue=settings.rb_email_queue_name,
    )
    email_worker = EmailWorker(
        publisher=email_publisher,
        render=messages_render,
    )

    workers: Dict[TargetWorkerName, Worker] = {
        "email": email_worker,
    }

    # history_worker выполняется для всех сообщений, поэтому он устанавливается
    # отдельно от указываемых в сообщениях
    history_publisher = HistoryPublisher(
        coninfo="",
        query="",
    )
    history_worker = HistoryWorker(publisher=history_publisher, render=messages_render)

    subscriber = Consumer(
        workers=workers,
        history_worker=history_worker,
        subscriber_channel=subscriber_channel,
        subscriber_queue_name=settings.rb_worker_queue_name,
    )

    return WorkerApp(subscriber=subscriber)
