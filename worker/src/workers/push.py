from typing import Optional

from errors.exceptions import NoPushIdForPushWorkerError
from workers.worker import Worker, WorkerMessage


class PushWorker(Worker):
    """Воркер обрабатывающий SMS."""

    @property
    def templates_target_name(self) -> str:
        """Целевой способ доставки сообщений.

        Returns:
            str: Способ.
        """
        return "push"

    def get_client_id_from_message(self, message: WorkerMessage) -> str:
        """Получить email клиента для публикации.

        Args:
            message (WorkerMessage): Сообщение, из которого извлечь push_id.

        Returns:
            str: push_id.

        Raises:
            NoPushIdForPushWorkerError: Если id не указан.
        """
        push_id: Optional[str] = message.push_id
        if push_id is None:
            raise NoPushIdForPushWorkerError()
        return push_id
