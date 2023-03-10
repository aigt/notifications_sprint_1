import json
import logging
from typing import Generator

import pytest
from deepdiff import DeepDiff
from pika.adapters.blocking_connection import BlockingChannel


def test_email_info(
    rabbit_pub_channel: BlockingChannel,
    rabbit_sub_channel: BlockingChannel,
    templates_db: Generator,
    empty_history_db: Generator,
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
      "telephone": "12345678901",
      "push_id": "fhgfghfhfh",
      "template": "info",
      "fields": {
        "title": "Привет.",
        "text": "Это текст."
      }
    }
    """
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
        assert body is not None, "Consumed message is None"

        if body is not None:
            message = json.loads(body.decode())
            logging.info(message)

            expected_message = {
                "email": "email@host.com",
                "content": '<!DOCTYPE html><html lang="ru"><head><title>Для информации.</title></head><body><h1>Привет.</h1><p>Это текст.</p></body></html>',
            }

            assert not DeepDiff(message, expected_message, ignore_order=True)

            rabbit_sub_channel.basic_ack(_method_frame.delivery_tag)
            break


def test_sms_info(
    rabbit_pub_channel: BlockingChannel,
    rabbit_sub_channel: BlockingChannel,
    templates_db: Generator,
    empty_history_db: Generator,
) -> None:
    worker_queue = "worker"
    pub_queue = "sms"
    notify_exchange = "notifications"
    pub_body = """{
      "targets": [
        "sms"
      ],
      "email": "email@host.com",
      "telephone": "12345678901",
      "push_id": "fhgfghfhfh",
      "user_id": "3a815b88-c88e-4381-bcc6-fea73f052946",
      "template": "info",
      "fields": {
        "title": "Привет.",
        "text": "Это текст."
      }
    }
    """
    rabbit_pub_channel.exchange_declare(exchange=notify_exchange, durable=True)
    rabbit_pub_channel.queue_declare(queue=worker_queue, durable=True)
    rabbit_sub_channel.queue_declare(queue=pub_queue, durable=True)
    rabbit_pub_channel.queue_bind(queue=worker_queue, exchange=notify_exchange)
    rabbit_pub_channel.basic_publish(
        exchange=notify_exchange,
        routing_key=worker_queue,
        body=pub_body,
    )

    for _method_frame, _properties, body in rabbit_sub_channel.consume(
        queue=pub_queue,
        auto_ack=False,
        inactivity_timeout=15,
    ):
        assert body is not None, "Consumed message is None"

        if body is not None:
            message = json.loads(body.decode())
            logging.info(message)

            expected_message = {
                "sms": "12345678901",
                "content": "Привет.\\n\\nЭто текст.",
            }

            assert not DeepDiff(message, expected_message, ignore_order=True)

            rabbit_sub_channel.basic_ack(_method_frame.delivery_tag)
            break


def test_push_info(
    rabbit_pub_channel: BlockingChannel,
    rabbit_sub_channel: BlockingChannel,
    templates_db: Generator,
    empty_history_db: Generator,
) -> None:
    worker_queue = "worker"
    pub_queue = "push"
    notify_exchange = "notifications"
    pub_body = """{
      "targets": [
        "push"
      ],
      "email": "email@host.com",
      "telephone": "12345678901",
      "push_id": "fhgfghfhfh",
      "user_id": "3a815b88-c88e-4381-bcc6-fea73f052946",
      "template": "info",
      "fields": {
        "title": "Привет.",
        "text": "Это текст."
      }
    }
    """
    rabbit_pub_channel.exchange_declare(exchange=notify_exchange, durable=True)
    rabbit_pub_channel.queue_declare(queue=worker_queue, durable=True)
    rabbit_sub_channel.queue_declare(queue=pub_queue, durable=True)
    rabbit_pub_channel.queue_bind(queue=worker_queue, exchange=notify_exchange)
    rabbit_pub_channel.basic_publish(
        exchange=notify_exchange,
        routing_key=worker_queue,
        body=pub_body,
    )

    for _method_frame, _properties, body in rabbit_sub_channel.consume(
        queue=pub_queue,
        auto_ack=False,
        inactivity_timeout=15,
    ):
        assert body is not None, "Consumed message is None"

        if body is not None:
            message = json.loads(body.decode())
            logging.info(message)

            expected_message = {
                "push_id": "fhgfghfhfh",
                "content": "Привет.\\n\\nЭто текст.",
            }

            assert not DeepDiff(message, expected_message, ignore_order=True)

            rabbit_sub_channel.basic_ack(_method_frame.delivery_tag)
            break
