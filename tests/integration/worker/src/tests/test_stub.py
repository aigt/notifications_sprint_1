import pika
import pytest
from pika.adapters.blocking_connection import BlockingChannel


def test_stub(
    rabbit_pub_channel: BlockingChannel,
    rabbit_sub_channel: BlockingChannel,
) -> None:
    QUEUE = "fgh"
    EXCHANGE = "fgh"
    BODY = "hello"
    rabbit_pub_channel.queue_declare(queue=QUEUE, durable=False)
    rabbit_pub_channel.exchange_declare(exchange=EXCHANGE, durable=False)
    rabbit_pub_channel.queue_bind(queue=QUEUE, exchange=EXCHANGE)

    rabbit_pub_channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=QUEUE,
        body=BODY,
        properties=pika.spec.BasicProperties(content_type="text/plain"),
    )

    for _method_frame, _properties, body in rabbit_sub_channel.consume(
        QUEUE,
        inactivity_timeout=10,
    ):
        assert body.decode() == BODY
        break
