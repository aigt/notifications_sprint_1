import logging

import backoff
import psycopg
from cachetools.func import ttl_cache  # type: ignore
from psycopg import sql
from psycopg.errors import Error
from psycopg.rows import dict_row

from errors.exceptions import NoNecessaryTemplateError


class TemplatesStorage:
    """Хранилище шаблонов."""

    def __init__(self, coninfo: str, query: str) -> None:
        self._coninfo = coninfo
        self._query = query

    @ttl_cache(ttl=15 * 60)  # noqa: WPS432
    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=Error,
        logger=logging.getLogger("my_logger"),
        max_time=20,  # noqa: WPS432
    )
    def get(self, name: str, target: str) -> str:
        """Получить шаблон по названию.

        Args:
            name (str): Название шаблона.
            target (str): Шаблон под какую публикацию (email, sms и тп.).

        Returns:
            str: Шаблон.

        Raises:
            NoNecessaryTemplateError: Если необходимый шаблон не найден.
        """
        logging.info(
            "Loading and caching template: %s, for target: %s",  # noqa: WPS323
            name,
            target,
        )

        sql_query = sql.SQL(self._query).format(table_name=sql.Identifier(target))
        logging.info(
            "SQL query: %s",  # noqa: WPS323
            sql_query,
        )

        with psycopg.connect(self._coninfo) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    sql_query,
                    (name,),
                )

                template: dict = cursor.fetchone()
                logging.info(
                    "Template: %s",  # noqa: WPS323
                    template,
                )

                if not template:
                    raise NoNecessaryTemplateError()

                return template["template"]  # type: ignore
