from errors.exceptions import NoEmailForEmailWorkerError
from services.email_publisher import EmailPublisher
from services.email_render import EmailRender
from workers.worker import Worker, WorkerMessage


class EmailWorker(Worker):
    """Воркер обрабатывающий Email."""

    def __init__(
        self,
        email_publisher: EmailPublisher,
        email_render: EmailRender,
    ) -> None:
        self._email_publisher = email_publisher
        self._email_render = email_render

    def run(self, message: WorkerMessage) -> None:
        """Обработать сообщение.

        Args:
            message (WorkerMessage): Сообщение для обработки.

        Raises:
            NoEmailForEmailWorkerError: Если не указан email
        """
        if not message.email:
            raise NoEmailForEmailWorkerError()

        rendered_email = self._email_render.render_email(
            template=message.template,
            fields=message.fields,
        )

        self._email_publisher.publish(
            email=message.email,
            email_content=rendered_email,
        )
