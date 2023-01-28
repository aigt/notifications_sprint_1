import time

import orjson
from grpc_test_server.users_data import users_data
from pika.adapters.blocking_connection import BlockingChannel
from settings import get_settings
from testdata.notifications import info
from utils.send_data import send

settings = get_settings()


def test_info(rabbit_channel: BlockingChannel, add_bookmark: None) -> None:
    """Проверка доставки info уведомления из очереди generator в очередь worker."""
    send(rabbit_channel, settings.rb_receiving_queue, info.json().encode())
    time.sleep(3)
    for user_data in users_data:
        method_frame, _, body = rabbit_channel.basic_get(settings.rb_transfer_queue, auto_ack=True)
        payload = orjson.loads(body)
        assert payload.get("fields") == info.fields
        assert payload.get("user_id") == user_data[0]
        assert payload.get("email") == user_data[1]
