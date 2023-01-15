from services.consumer import Consumer


class WorkerApp:
    """Приложение Worker."""

    def __init__(self, consumer: Consumer) -> None:
        self._consumer = consumer

    def run(self) -> None:
        """Запустить приожение."""
        self._consumer.run()
