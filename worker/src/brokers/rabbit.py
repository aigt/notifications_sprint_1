import logging
from time import sleep
from typing import Optional

from pika import BlockingConnection, ConnectionParameters
from pika.credentials import PlainCredentials
from pika.exceptions import AMQPConnectionError

from errors.exceptions import RabbitMQConnectionIsNotInitializedError


class RabbitMQ:
    """Клиент для работы с RabbitMQ."""

    def __init__(
        self,
        host: str,
        port: int,
        credentials: PlainCredentials,
        max_tries_to_connect: int,
        connect_retry_period: int,
    ) -> None:
        self._host = host
        self._port = port
        self._credentials = credentials
        self._max_tries_to_connect = max_tries_to_connect
        self._connect_retry_period = connect_retry_period

        self._connection: Optional[BlockingConnection] = None

    @property
    def connection(self) -> BlockingConnection:
        """Соединение с RabbitMQ.

        Raises:
            RabbitMQConnectionIsNotInitializedError: Если соединение не установлено.

        Returns:
            BlockingConnection: Соединение с RabbitMQ.
        """
        if self._connection is None:
            raise RabbitMQConnectionIsNotInitializedError()
        return self._connection

    def connect(self) -> None:  # noqa: WPS231
        """Установить соединение с RabbitMQ.

        Raises:
            AMQPConnectionError: Ошибка соединения если количество попыток истекло.
        """
        logging.info("Connecting to RabbitMQ")
        connection = None
        try_num = 0
        conn_params = ConnectionParameters(
            host=self._host,
            port=self._port,
            credentials=self._credentials,
        )
        while not connection:
            try:
                self._connection = BlockingConnection(conn_params)
                break
            except AMQPConnectionError as connection_ex:
                logging.info(
                    "Connection #%s faild (retry in %s second)",  # noqa: WPS323
                    try_num,
                    self._connect_retry_period,
                )
                try_num += 1
                if try_num >= self._max_tries_to_connect:
                    raise connection_ex
                sleep(self._connect_retry_period)
        logging.info("RabbitMQ connected")

    def close_connection(self) -> None:
        """Закрыть соединение с RabbitMQ.

        Raises:
            RabbitMQConnectionIsNotInitializedError: Соединение не установлено.
        """
        if self._connection is None:
            raise RabbitMQConnectionIsNotInitializedError()
        self._connection.close()
        self._connection = None
