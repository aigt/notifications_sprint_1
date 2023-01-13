class RabbitMQConnectionIsNotInitializedError(Exception):
    """Соединение RabbitMQ не инициализировано."""


class NoRequiredWorkerError(Exception):
    """Нет необходимых воркеров для сообщения."""


class NoEmailForEmailWorkerError(Exception):
    """Не указан email в сообщении на отправку электронной почтой."""


class NoNecessaryTemplateError(Exception):
    """Нет запрашиваемого шаблона."""


class PostgresDBConnectionIsNotInitializedError(Exception):
    """Соединение PostgresDB не инициализировано."""
