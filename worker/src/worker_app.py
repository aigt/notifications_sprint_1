from services.subscriber import Subscriber


class WorkerApp:
    """Приложение Worker."""

    def __init__(self, subscriber: Subscriber) -> None:
        self._subscriber = subscriber

    def run(self) -> None:
        """Запустить приожение."""
        self._subscriber.run()
