class RabbitMQConnectionIsNotInitializedError(Exception):
    """Соединение RabbitMQ не инициализировано."""


class NoRequiredWorkerError(Exception):
    """Нет необходимых воркеров для сообщения."""


class NoEmailForEmailWorkerError(Exception):
    """Не указан email в сообщении на отправку электронной почтой."""


class NoUserIdForHistoryWorkerError(Exception):
    """Не указан user_id в сообщении необходимый для сохранения истории."""


class NoNecessaryTemplateError(Exception):
    """Нет запрашиваемого шаблона."""


class PostgresDBConnectionIsNotInitializedError(Exception):
    """Соединение PostgresDB не инициализировано."""
