import logging
from abc import ABC, abstractmethod

from services.publishers.publisher import Publisher
from services.render import Render
from workers.worker_message import WorkerMessage


class Worker(ABC):
    """Воркер выполняющий задачу."""

    def __init__(
        self,
        publisher: Publisher,
        render: Render,
    ) -> None:
        self._publish = publisher
        self._render = render

    @property
    @abstractmethod
    def templates_target_name(self) -> str:
        """Целевой способ доставки сообщений.

        Returns:
            str: Способ.
        """

    @abstractmethod
    def get_client_id_from_message(self, message: WorkerMessage) -> str:
        """Получить идентификатор клиента для публикации.

        Args:
            message (WorkerMessage): Сообщение, из которого извлечь идентификатор.

        Returns:
            str: Идентификатор.
        """

    def run(self, message: WorkerMessage) -> None:
        """Обработать сообщение.

        Args:
            message (WorkerMessage): Сообщение для обработки.
        """
        logging.info(
            "Worker start to process %s message: %s",  # noqa: WPS323
            self.templates_target_name,
            message,
        )

        rendered_message = self._render(
            template=message.template,
            target=self.templates_target_name,
            fields=message.fields,
        )

        logging.info(
            "Worker rendered %s: %s",  # noqa: WPS323
            self.templates_target_name,
            rendered_message,
        )

        self._publish(
            client_id=self.get_client_id_from_message(message=message),
            message_content=rendered_message,
        )

        logging.info(
            "Worker published %s",  # noqa: WPS323
            self.templates_target_name,
        )
