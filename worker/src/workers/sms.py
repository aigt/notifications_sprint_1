from typing import Optional

from errors.exceptions import NoTelephoneForSMSWorkerError
from workers.worker import Worker, WorkerMessage


class SMSWorker(Worker):
    """Воркер обрабатывающий SMS."""

    @property
    def templates_target_name(self) -> str:
        """Целевой способ доставки сообщений.

        Returns:
            str: Способ.
        """
        return "sms"

    def get_client_id_from_message(self, message: WorkerMessage) -> str:
        """Получить email клиента для публикации.

        Args:
            message (WorkerMessage): Сообщение, из которого извлечь email.

        Returns:
            str: Телефон.

        Raises:
            NoTelephoneForSMSWorkerError: Если телефон не указан.
        """
        telephone: Optional[str] = message.telephone
        if telephone is None:
            raise NoTelephoneForSMSWorkerError()
        return telephone
