class RabbitMQConnectionIsNotInitializedError(Exception):
    """Соединение RabbitMQ не инициализировано."""


class NoRequiredWorkerError(Exception):
    """Нет необходимых воркеров для сообщения."""
