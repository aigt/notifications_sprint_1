import orjson
from models.notification import Meta, Notification
from notification_handler.notification_handler import NotificationHandler
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


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
    meta = notification.get("meta")
    notification = Notification(
        meta=Meta(**meta),
        type=notification.get("type"),
        custom_template=notification.get("custom_template"),
        fields=notification.get("fields"),
    )

    sorter = NotificationHandler()
    sorter.sort(notification)

    ch.basic_ack(delivery_tag=method.delivery_tag)
