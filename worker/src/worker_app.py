from services.consumer import Consumer


class WorkerApp:
    """Приложение Worker."""

    def __init__(self, subscriber: Consumer) -> None:
        self._subscriber = subscriber

    def run(self) -> None:
        """Запустить приожение."""
        self._subscriber.run()
