import logging
from typing import Dict

from jinja2 import BaseLoader, Environment

from services.templates_storage import TemplatesStorage
from workers.worker import MessageFieldName, MessageFieldValue


class EmailRender:
    """Сервис рендеринга email сообщений."""

    loader = BaseLoader()
    templates_target_name = "email"

    def __init__(
        self,
        templates_storage: TemplatesStorage,
    ) -> None:
        self._templates_storage = templates_storage

    def render_email(
        self,
        template: str,
        fields: Dict[MessageFieldName, MessageFieldValue],
    ) -> str:
        """Рендерить Email.

        Args:
            template (str): Шаблон письма.
            fields (Dict[MessageFieldName, MessageFieldValue]): Поля письма для заполнения шаблона.

        Returns:
            str: Письмо.
        """
        logging.info(
            "Rendering email with template: %s, and fields: %s",  # noqa: WPS323
            template,
            fields,
        )
        str_template = self._templates_storage.get(
            name=template,
            target=self.templates_target_name,
        )

        logging.info(
            "Got template: %s",  # noqa: WPS323
            str_template,
        )
        jinja_env = Environment(
            loader=self.loader,
            autoescape=True,
        )
        jinja_template = jinja_env.from_string(
            str_template,
        )
        return jinja_template.render(**fields)  # type: ignore
