import time

import orjson
from pika.adapters.blocking_connection import BlockingChannel
from testdata.notifications import welcome_1
from utils.send_data import send

from models.notification import Meta, NotificationForWorker


def test_welcome(rabbit_channel: BlockingChannel) -> None:
    """Проверка доставки Welcome уведомления из очереди generator в очередь worker."""

    send(rabbit_channel, "generator", welcome_1.json().encode())
    time.sleep(3)
    method_frame, _, body = rabbit_channel.basic_get("worker")

    payload = orjson.loads(body)

    notification_in_worker_queue = NotificationForWorker(
        email=payload.get("email"),
        template=payload.get("template"),
        fields=payload.get("fields"),
    )

    assert welcome_1.meta.email == notification_in_worker_queue.email
    assert welcome_1.type.value == notification_in_worker_queue.template
    assert str(welcome_1.fields.get("user_name")) == notification_in_worker_queue.fields.get("user_name")
    assert str(welcome_1.fields.get("user_id")) == notification_in_worker_queue.fields.get("user_id")

    rabbit_channel.basic_ack(method_frame.delivery_tag)
