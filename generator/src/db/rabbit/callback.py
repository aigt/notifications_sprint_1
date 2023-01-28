import orjson
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from core.settings import get_settings
from db.mongo.mongo import get_mongo
from db.rabbit.rabbitmq import get_rabbit
from generator.generator import Generator
from models.notifications import Meta, NotificationFromNotifications
from services.auth_data_client import AuthDataClient

settings = get_settings()


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

    generator = Generator(
        queue=get_rabbit(),
        ugc_base=get_mongo(),
        auth_data_client=AuthDataClient(settings.auth_host),
    )
    generator.create_data_for_worker(notification)

    ch.basic_ack(delivery_tag=method.delivery_tag)
