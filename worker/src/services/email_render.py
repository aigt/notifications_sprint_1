from typing import Dict

from jinja2 import BaseLoader, Environment

from services import template_storage
from workers.worker import MessageFieldName, MessageFieldValue


class EmailRender:
    """Сервис рендеринга email сообщений."""

    loader = BaseLoader()

    @classmethod
    def render_email(
        cls,
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
        str_template = template_storage.get(template)
        jinja_template = Environment(loader=cls.loader, autoescape=True).from_string(
            str_template,
        )
        return jinja_template.render(**fields)  # type: ignore
