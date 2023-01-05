import time

import orjson
from pika.adapters.blocking_connection import BlockingChannel
from testdata.notifications import welcome_1
from utils.send_data import send

from models.notification import Meta, Notification


def test_welcome(rabbit_channel: BlockingChannel) -> None:
    """Проверка доставки Welcome уведомления из очереди Notification в очередь Generator."""

    send(rabbit_channel, "Notification", welcome_1.json().encode())
    time.sleep(1)
    method_frame, _, body = rabbit_channel.basic_get("Generator")

    payload = orjson.loads(body)

    meta = Meta(**payload.get("meta"))

    notification_in_generator_queue = Notification(
        meta=meta,
        type=payload.get("type"),
        custom_template=payload.get("custom_template"),
        fields=payload.get("fields"),
    )

    assert notification_in_generator_queue == welcome_1
    rabbit_channel.basic_ack(method_frame.delivery_tag)
