import logging
from typing import Generator

import pytest
from pika.adapters.blocking_connection import BlockingChannel


def test_stub(
    rabbit_pub_channel: BlockingChannel,
    rabbit_sub_channel: BlockingChannel,
    templates_db: Generator,
) -> None:
    worker_queue = "worker"
    email_queue = "email"
    notify_exchange = "notifications"
    pub_body = """{
  "targets": [
    "email"
  ],
  "email": "email@host.com",
  "user_id": "3a815b88-c88e-4381-bcc6-fea73f052946",
  "template": "info",
  "fields": {
    "title": "Привет.",
    "text": "Это текст."
  }
}"""
    rabbit_pub_channel.exchange_declare(exchange=notify_exchange, durable=True)
    rabbit_pub_channel.queue_declare(queue=worker_queue, durable=True)
    rabbit_sub_channel.queue_declare(queue=email_queue, durable=True)
    rabbit_pub_channel.queue_bind(queue=worker_queue, exchange=notify_exchange)
    rabbit_pub_channel.basic_publish(
        exchange=notify_exchange,
        routing_key=worker_queue,
        body=pub_body,
    )

    for _method_frame, _properties, body in rabbit_sub_channel.consume(
        queue=email_queue,
        auto_ack=False,
        inactivity_timeout=15,
    ):
        logging.info(body)
        assert (
            body
            == b'{"email":"email@host.com","content":"<!DOCTYPE html><html lang=\\"ru\\"><head><title>\\u0414\\u043b\\u044f \\u0438\\u043d\\u0444\\u043e\\u0440\\u043c\\u0430\\u0446\\u0438\\u0438.</title></head><body><h1>\\u041f\\u0440\\u0438\\u0432\\u0435\\u0442.</h1><p>\\u042d\\u0442\\u043e \\u0442\\u0435\\u043a\\u0441\\u0442.</p></body></html>"}'
        )
        rabbit_sub_channel.basic_ack(_method_frame.delivery_tag)
        break
