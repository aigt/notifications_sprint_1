from workers.worker import Worker, WorkerMessage


class HistoryWorker(Worker):
    """Воркер заносящий оповещения в историю."""

    def run(self, message: WorkerMessage) -> None:
        """Обработать сообщение.

        Args:
            message (WorkerMessage): Сообщение для обработки.
        """
        return  # noqa: WPS324
