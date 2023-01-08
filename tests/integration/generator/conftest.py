import logging
from time import sleep
from typing import Generator

import pika
import requests  # type: ignore
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPError
from pytest import fixture
from settings import get_settings

settings = get_settings()


@fixture(scope="session")
def rabbit_con() -> Generator[BlockingConnection, None, None]:
    """Соединение с RabbitMQ.

    Yields:
        BlockingConnection: Соединение с RabbitMQ.
    """
    credentials = pika.PlainCredentials(settings.rb_user, settings.rb_password)
    logging.info("Connecting to RabbitMQ")
    connection = None
    try_num = 0
    while not connection:
        try:
            connection = BlockingConnection(
                ConnectionParameters(host=settings.rb_host, port=settings.rb_port, credentials=credentials),
            )
            break
        except AMQPError as ex:
            logging.info("Connection #%s faild (retry in 1 second)", try_num)
            try_num += 1
            if try_num >= 20:
                raise ex
            sleep(1)
            continue

    logging.info("RabbitMQ connected")

    yield connection
    connection.close(reply_code=200, reply_text="Normal shutdown")


@fixture(scope="function")
def rabbit_channel(rabbit_con: BlockingConnection) -> Generator[BlockingChannel, None, None]:
    """Канал RabbitMQ.

    Yields:
        BlockingChannel: Канал RabbitMQ.
    """
    channel = rabbit_con.channel()
    yield channel
    channel.close(reply_code=0, reply_text="Normal shutdown")
