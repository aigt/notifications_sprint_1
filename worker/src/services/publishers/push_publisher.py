import logging

from services.publishers.queue_publisher import QueuePublisher


class PushPublisher(QueuePublisher):
    """Сервис публикации SMS в очередь."""

    def __call__(self, client_id: str, message_content: str) -> None:
        """Добавить в очередь на отправку push-уведомления.

        Args:
            client_id (str): push_id, на который отправить сообщение.
            message_content (str): Содержимое SMS.
        """
        message = {"push_id": client_id, "content": message_content}
        self._publish(message=message)

        logging.info("Worker PushPublisher published push message")
