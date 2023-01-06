import orjson
from models.notifications import Meta, NotificationFromNotifications
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
    notification = NotificationFromNotifications(
        meta=Meta(**meta),
        type=notification.get("type"),
        custom_template=notification.get("custom_template"),
        fields=notification.get("fields"),
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)
