import logging

from services.publishers.queue_publisher import QueuePublisher


class SMSPublisher(QueuePublisher):
    """Сервис публикации SMS в очередь."""

    def __call__(self, client_id: str, message_content: str) -> None:
        """Добавить в очередь на отправку SMS.

        Args:
            client_id (str): телефон, на который отправить сообщение.
            message_content (str): Содержимое SMS.
        """
        message = {"sms": client_id, "content": message_content}
        self._publish(message=message)

        logging.info("Worker SMSPublisher published SMS message")
