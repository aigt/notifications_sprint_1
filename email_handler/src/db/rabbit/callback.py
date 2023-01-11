import orjson
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from sender.email_sender import send_message

from models.notification import NotificationEmail


def callback(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes,
) -> None:
    """Обработка и передача поступающих данных в функцию отправки сообщений.

    Args:
        ch(BlockingChannel): Rabbitmq канал
        method(Basic.Deliver): Доставщик
        properties(BasicProperties): Свойства
        body(bytes): Тело данных из очереди
    """
    body_json = orjson.loads(body)
    notification = NotificationEmail(**body_json)
    send_message(email=notification.email, content=notification.content)
    ch.basic_ack(delivery_tag=method.delivery_tag)
