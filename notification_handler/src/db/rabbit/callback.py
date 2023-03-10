import orjson
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from db.postgres.postgres import get_postgres
from db.rabbit.rabbitmq import get_rabbit
from models.notification import Meta, Notification
from notification_handler.notification_handler import NotificationHandler


def callback(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes,
) -> None:
    """Обработка и передача поступающих данных в сортировщик.

    Args:
        ch(BlockingChannel): Rabbitmq канал
        method(Basic.Deliver): Доставщик
        properties(BasicProperties): Свойства
        body(bytes): Тело данных из очереди
    """
    notification = orjson.loads(body)
    notification["meta"] = Meta(**notification.get("meta"))
    notification = Notification(**notification)

    sorter = NotificationHandler(db=get_postgres(), queue=get_rabbit())
    sorter.sort(notification)

    ch.basic_ack(delivery_tag=method.delivery_tag)
