import time

import orjson
from pika.adapters.blocking_connection import BlockingChannel
from settings import get_settings
from testdata.notifications import welcome_1
from utils.send_data import send

from models.notification import Meta, TaskForWorker

settings = get_settings()


def test_welcome(rabbit_channel: BlockingChannel) -> None:
    """Проверка доставки Welcome уведомления из очереди generator в очередь worker."""

    send(rabbit_channel, settings.rb_receiving_queue, welcome_1.json().encode())
    time.sleep(3)
    method_frame, _, body = rabbit_channel.basic_get(settings.rb_transfer_queue)

    payload = orjson.loads(body)

    notification_in_worker_queue = TaskForWorker(
        email=payload.get("email"),
        template=payload.get("template"),
        fields=payload.get("fields"),
        targets=["email"],
    )

    assert welcome_1.fields.get("email") == notification_in_worker_queue.email
    assert welcome_1.type.value == notification_in_worker_queue.template
    assert str(welcome_1.fields.get("user_name")) == notification_in_worker_queue.fields.get("user_name")
    assert str(welcome_1.fields.get("user_id")) == notification_in_worker_queue.fields.get("user_id")

    rabbit_channel.basic_ack(method_frame.delivery_tag)
