from typing import Optional

from errors.exceptions import NoEmailForEmailWorkerError
from workers.worker import Worker, WorkerMessage


class EmailWorker(Worker):
    """Воркер обрабатывающий Email."""

    @property
    def templates_target_name(self) -> str:
        """Целевой способ доставки сообщений.

        Returns:
            str: Способ.
        """
        return "email"

    def get_client_id_from_message(self, message: WorkerMessage) -> str:
        """Получить email клиента для публикации.

        Args:
            message (WorkerMessage): Сообщение, из которого извлечь email.

        Returns:
            str: Email.

        Raises:
            NoEmailForEmailWorkerError: Если Email не указан.
        """
        email: Optional[str] = message.email
        if email is None:
            raise NoEmailForEmailWorkerError()
        return email
