from typing import Dict

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from brokers.rabbit import RabbitMQ
from errors.exceptions import NoRequiredWorkerError
from workers.worker import TargetWorkerName, Worker, WorkerMessage


class Subscriber:
    """Подписчик."""

    def __init__(
        self,
        workers: Dict[TargetWorkerName, Worker],
        history_worker: Worker,
        rabbit: RabbitMQ,
    ) -> None:
        self._workers = workers
        self._history_worker = history_worker
        self._rabbit = rabbit

    def run(self) -> None:
        """Подписаться на поступающие задачи."""
        self._rabbit.connect()
        channel = self._rabbit.connection.channel()
        channel.basic_consume(queue="test", on_message_callback=self._on_message)
        try:
            channel.start_consuming()
        except Exception:
            channel.stop_consuming()
        channel.close(reply_code=0, reply_text="Normal shutdown")

    def _on_message(
        self,
        channel: BlockingChannel,
        method_frame: Basic.Deliver,
        header_frame: BasicProperties,
        body: bytes,
    ) -> None:
        """Обработка сообщений поступающих из очереди.

        Args:
            channel (BlockingChannel): Канал получения сообщений.
            method_frame (Basic.Deliver): Method Frame.
            header_frame (BasicProperties): Header Frame.
            body (bytes): Тело сообщения.

        Raises:
            NoRequiredWorkerError: Если целевой воркер отсутствует.
        """
        message = WorkerMessage.parse_raw(body.decode())
        for target_worker in message.targets:
            if target_worker not in self._workers:
                raise NoRequiredWorkerError(
                    "No required worker {target_worker}".format(
                        target_worker=target_worker,
                    ),
                )
            worker = self._workers[target_worker]
            worker.run(message)
        self._history_worker.run(message)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
