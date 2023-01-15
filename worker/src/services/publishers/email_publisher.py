import logging

from services.publishers.queue_publisher import QueuePublisher


class EmailPublisher(QueuePublisher):
    """Сервис публикации писем в очередь."""

    def __call__(self, client_id: str, message_content: str) -> None:
        """Добавить в очередь на отправку письмо.

        Args:
            client_id (str): Email, на который отправить письмо.
            message_content (str): Содержимое письма.
        """
        message = {"email": client_id, "content": message_content}
        self._publish(message=message)

        logging.info("Worker EmailPublisher published email message")
