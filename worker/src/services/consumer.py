import logging
from typing import Dict

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from errors.exceptions import NoRequiredWorkerError
from workers.worker import Worker
from workers.worker_message import TargetWorkerName, WorkerMessage


class Consumer:
    """Потребитель из очереди."""

    def __init__(
        self,
        workers: Dict[TargetWorkerName, Worker],
        history_worker: Worker,
        subscriber_channel: BlockingChannel,
        subscriber_queue_name: str,
    ) -> None:
        self._workers = workers
        self._history_worker = history_worker
        self._subscriber_channel = subscriber_channel
        self._subscriber_queue_name = subscriber_queue_name

    def run(self) -> None:
        """Подписаться на поступающие задачи."""
        self._subscriber_channel.basic_consume(
            queue=self._subscriber_queue_name,
            on_message_callback=self._on_message,
        )
        try:
            self._subscriber_channel.start_consuming()
        except Exception:
            self._subscriber_channel.stop_consuming()
        self._subscriber_channel.close(reply_code=0, reply_text="Normal shutdown")

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
        logging.info("Worker got message:")
        logging.info(body)
        message = WorkerMessage.parse_raw(body)
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
