from abc import ABC, abstractmethod


class Publisher(ABC):
    """Абстрактный сервис публикации."""

    @abstractmethod
    def __call__(self, client_id: str, message_content: str) -> None:
        """Опубликовать контент.

        Args:
            client_id (str): Id клиента в сервисе отправки.
            message_content (str): Содержимое для отправки.
        """
