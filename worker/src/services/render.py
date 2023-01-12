import logging
from typing import Dict

from jinja2 import BaseLoader, Environment

from services.templates_storage import TemplatesStorage
from workers.worker import MessageFieldName, MessageFieldValue


class Render:
    """Сервис рендеринга сообщений."""

    loader = BaseLoader()
    jinja_env = Environment(
        loader=loader,
        autoescape=True,
    )

    def __init__(
        self,
        templates_storage: TemplatesStorage,
    ) -> None:
        self._templates_storage = templates_storage

    def __call__(
        self,
        template: str,
        target: str,
        fields: Dict[MessageFieldName, MessageFieldValue],
    ) -> str:
        """Рендерить Email.

        Args:
            template (str): Шаблон письма.
            target (str): Шаблон Для какого способа публикации.
            fields (Dict[MessageFieldName, MessageFieldValue]): Поля письма для заполнения шаблона.

        Returns:
            str: Сообщение в соответствии с шаблоном.
        """
        logging.info(
            "Rendering email with template: %s, and fields: %s",  # noqa: WPS323
            template,
            fields,
        )

        str_template = self._templates_storage.get(
            name=template,
            target=target,
        )

        logging.info(
            "Got template: %s",  # noqa: WPS323
            str_template,
        )

        jinja_template = self.jinja_env.from_string(
            str_template,
        )

        return jinja_template.render(**fields)  # type: ignore
