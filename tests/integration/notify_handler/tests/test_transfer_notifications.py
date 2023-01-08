import time

import orjson
from pika.adapters.blocking_connection import BlockingChannel
from psycopg.cursor import Cursor
from settings import get_settings
from testdata.notifications import mass_1, personal_1, welcome_1
from utils.postgres_requests import (
    get_mass_notification,
    get_personal_notification,
    notification_format,
)
from utils.send_data import send

from models.notification import Meta, Notification

settings = get_settings()


def test_immediate_notification(rabbit_channel: BlockingChannel) -> None:
    """Проверка доставки immediate уведомления из очереди notification в очередь Generator."""

    send(rabbit_channel, settings.rb_receiving_queue, welcome_1.json().encode())
    time.sleep(3)
    method_frame, _, body = rabbit_channel.basic_get(settings.rb_transfer_queue)

    payload = orjson.loads(body)

    payload["meta"] = Meta(**payload.get("meta"))

    notification_in_generator_queue = Notification(**payload)

    assert notification_in_generator_queue == welcome_1
    rabbit_channel.basic_ack(method_frame.delivery_tag)


def test_individual_notification(rabbit_channel: BlockingChannel, postgres_cur: Cursor) -> None:
    """Проверка доставки individual уведомления из очереди notification в базу notification_db"""

    send(rabbit_channel, settings.rb_receiving_queue, personal_1.json().encode())
    time.sleep(3)

    in_postgres = get_personal_notification(postgres_cur, personal_1.json(), str(personal_1.user_id))
    notification_in_postgres = notification_format(in_postgres)

    assert personal_1 == notification_in_postgres


def test_mass_notification(rabbit_channel: BlockingChannel, postgres_cur: Cursor) -> None:
    """Проверка доставки mass уведомления из очереди notification в базу notification_db"""

    send(rabbit_channel, settings.rb_receiving_queue, mass_1.json().encode())
    time.sleep(3)

    in_postgres = get_mass_notification(postgres_cur, mass_1.json())
    notification_in_postgres = notification_format(in_postgres)

    assert mass_1 == notification_in_postgres
