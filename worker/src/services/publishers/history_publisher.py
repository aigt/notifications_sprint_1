import logging
from uuid import UUID

import backoff
import psycopg
from psycopg import sql
from psycopg.errors import Error
from psycopg.rows import dict_row

from services.publishers.publisher import Publisher


class HistoryPublisher(Publisher):
    """Сервис публикации истории сообщений в БД."""

    def __init__(self, coninfo: str, query: str) -> None:
        self._coninfo = coninfo
        self._query = query

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=Error,
        logger=logging.getLogger("my_logger"),
        max_time=20,  # noqa: WPS432
    )
    def __call__(self, client_id: str, message_content: str) -> None:
        """Опубликовать контент.

        Args:
            client_id (str): Id клиента в сервисе отправки.
            message_content (str): Содержимое для отправки.
        """
        logging.info(
            "Saving message of user %s, in History DB: %s",  # noqa: WPS323
            client_id,
            message_content,
        )

        sql_query = sql.SQL(self._query)
        logging.info(
            "SQL query: %s",  # noqa: WPS323
            sql_query,
        )

        with psycopg.connect(self._coninfo) as conn:
            with conn.cursor(row_factory=dict_row) as cursor:

                cursor.execute(
                    sql_query,
                    {
                        "user_id": UUID(client_id),
                        "notification": message_content,
                    },
                )

                last_item = cursor.fetchone()
                logging.info(
                    "Saved history message: %s",  # noqa: WPS323
                    last_item,
                )
