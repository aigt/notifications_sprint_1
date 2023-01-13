from typing import Optional

from errors.exceptions import NoUserIdForHistoryWorkerError
from workers.worker import Worker, WorkerMessage


class HistoryWorker(Worker):
    """Воркер заносящий оповещения в историю."""

    @property
    def templates_target_name(self) -> str:
        """Целевой способ доставки сообщений.

        Returns:
            str: Способ.
        """
        return "history"

    def get_client_id_from_message(self, message: WorkerMessage) -> str:
        """Получить идентификатор клиента для публикации.

        Args:
            message (WorkerMessage): Сообщение, из которого извлечь идентификатор.

        Returns:
            str: Идентификатор.

        Raises:
            NoUserIdForHistoryWorkerError: Если не указан user_id.
        """
        user_id: Optional[str] = message.fields.get("user_id", None)
        if user_id is None:
            raise NoUserIdForHistoryWorkerError()
        return user_id
