import logging
from time import sleep
from typing import Generator

import pika
import psycopg
import pymongo
import requests  # type: ignore
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPError
from psycopg import Cursor
from psycopg.rows import dict_row
from pymongo import MongoClient
from pytest import fixture
from settings import get_settings
from utils.add_mongo_data import add_test_data_bookmark
from utils.add_postgres_data import add_users

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


@fixture(scope="session")
def mongo_con() -> Generator:
    """Соединение с MongoDB"""

    client: pymongo.MongoClient = pymongo.MongoClient(get_settings().mongo_dsn, uuidRepresentation="standard")
    yield client
    client.close()


@fixture(scope="function")
def postgres_cur() -> Generator:
    """postgres курсор."""
    con = psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        row_factory=dict_row,
    )
    cur = con.cursor()
    yield cur
    con.close()


@fixture(scope="function")
def add_bookmark(mongo_con: MongoClient) -> Generator:
    """Фикстура для загрузки и очистки данных из коллекции bookmark."""
    add_test_data_bookmark(mongo_con)
    yield
    mongo_con.ugc_movies.bookmark.drop()


@fixture(scope="function")
def add_users_postgres(postgres_cur: Cursor) -> Generator:
    """Фикстура для загрузки и очистки данных из коллекции bookmark."""
    add_users(postgres_cur)
    yield
    postgres_cur.execute("DELETE FROM users_auth.users_data")
    postgres_cur.execute("DELETE FROM users_auth.users")
    postgres_cur.connection.commit()
