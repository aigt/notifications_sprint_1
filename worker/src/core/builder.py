import logging
from typing import Dict, Type

from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials

from brokers.rabbit import RabbitMQ
from core.config import Settings
from services import query_loader
from services.consumer import Consumer
from services.publishers.email_publisher import EmailPublisher
from services.publishers.history_publisher import HistoryPublisher
from services.publishers.push_publisher import PushPublisher
from services.publishers.queue_publisher import QueuePublisher
from services.publishers.sms_publisher import SMSPublisher
from services.render import Render
from services.templates_storage import TemplatesStorage
from worker_app import WorkerApp
from workers.email import EmailWorker
from workers.history import HistoryWorker
from workers.push import PushWorker
from workers.sms import SMSWorker
from workers.worker import Worker
from workers.worker_message import TargetWorkerName


def build_queued_worker(
    rabbit_connection: BlockingChannel,
    exchange_name: str,
    queue_name: str,
    messages_render: Render,
    publisherclass_to_instantiate: Type[QueuePublisher],
    workerclass_to_instantiate: Type[Worker],
) -> Worker:
    """Создать и внедрить зависимости в воркер публикующий сообщения в очередь.

    Args:
        rabbit_connection (BlockingChannel): Подключение RabbitMQ.
        exchange_name (str): Exchange.
        queue_name (str): Имя очереди для публикации.
        messages_render (Render): Рендер сообщений.
        publisherclass_to_instantiate (Type[QueuePublisher]): Класс публишера.
        workerclass_to_instantiate (Type[Worker]): Класс воркера для создания.

    Returns:
        Worker: Созданный воркер
    """
    worker_channel = rabbit_connection.channel()

    worker_channel.exchange_declare(
        exchange=exchange_name,
        durable=True,
    )

    worker_channel.queue_declare(
        queue=queue_name,
        durable=True,
    )

    worker_channel.queue_bind(
        queue=queue_name,
        exchange=exchange_name,
    )

    publisher = publisherclass_to_instantiate(
        email_rabbit_channel=worker_channel,
        exchange=exchange_name,
        queue=queue_name,
    )

    return workerclass_to_instantiate(
        publisher=publisher,
        render=messages_render,
    )


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
        "exchange_name: %s",  # noqa: WPS323
        settings.rb_exchange_name,
    )
    logging.info(
        "email_queue_name: %s",  # noqa: WPS323
        settings.rb_email_queue_name,
    )
    logging.info(
        "sms_queue_name: %s",  # noqa: WPS323
        settings.rb_sms_queue_name,
    )
    logging.info(
        "push_queue_name: %s",  # noqa: WPS323
        settings.rb_push_queue_name,
    )
    logging.info(
        "Templates DB host:port: %s:%s",  # noqa: WPS323
        settings.tdb_dsn.host,
        settings.tdb_dsn.port,
    )
    logging.info(
        "History DB host:port: %s:%s",  # noqa: WPS323
        settings.hdb_dsn.host,
        settings.hdb_dsn.port,
    )

    templates_query = query_loader.load_sql(settings.tdb_template_sql_query_file)
    add_history_query = query_loader.load_sql(settings.hdb_add_history_sql_query_file)

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

    consumer_channel = rabbit_connection.channel()
    consumer_channel.exchange_declare(
        exchange=settings.rb_exchange_name,
        durable=True,
    )
    consumer_channel.queue_declare(
        queue=settings.rb_worker_queue_name,
        durable=True,
    )
    consumer_channel.queue_bind(
        queue=settings.rb_worker_queue_name,
        exchange=settings.rb_exchange_name,
    )

    messages_render = Render(
        templates_storage=templates_storage,
    )

    email_worker = build_queued_worker(
        rabbit_connection=rabbit_connection,
        exchange_name=settings.rb_exchange_name,
        queue_name=settings.rb_email_queue_name,
        messages_render=messages_render,
        publisherclass_to_instantiate=EmailPublisher,
        workerclass_to_instantiate=EmailWorker,
    )

    sms_worker = build_queued_worker(
        rabbit_connection=rabbit_connection,
        exchange_name=settings.rb_exchange_name,
        queue_name=settings.rb_sms_queue_name,
        messages_render=messages_render,
        publisherclass_to_instantiate=SMSPublisher,
        workerclass_to_instantiate=SMSWorker,
    )

    push_worker = build_queued_worker(
        rabbit_connection=rabbit_connection,
        exchange_name=settings.rb_exchange_name,
        queue_name=settings.rb_push_queue_name,
        messages_render=messages_render,
        publisherclass_to_instantiate=PushPublisher,
        workerclass_to_instantiate=PushWorker,
    )

    workers: Dict[TargetWorkerName, Worker] = {
        "email": email_worker,
        "sms": sms_worker,
        "push": push_worker,
    }

    # history_worker выполняется для всех сообщений, поэтому он устанавливается
    # отдельно от указываемых в сообщениях
    history_publisher = HistoryPublisher(
        coninfo=settings.hdb_dsn,
        query=add_history_query,
    )
    history_worker = HistoryWorker(publisher=history_publisher, render=messages_render)

    consumer = Consumer(
        workers=workers,
        history_worker=history_worker,
        subscriber_channel=consumer_channel,
        subscriber_queue_name=settings.rb_worker_queue_name,
    )

    return WorkerApp(consumer=consumer)
