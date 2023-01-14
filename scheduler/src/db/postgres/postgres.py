from functools import lru_cache
from typing import Any, Optional

from psycopg import Connection
from psycopg.rows import dict_row

postgres_con: Optional[Connection] = None


@lru_cache
def get_postgres_con() -> Connection:
    """Фабрика для получения соединения с postgres.

    Returns:
        postgres_con(Connection): соединение с postgres
    """
    return postgres_con


class Postgres:
    """Класс для работы с Postgres."""

    def __init__(self, connect: Connection):
        self._con = connect

    def read_notifications(self) -> Any:
        """Чтение данных из очереди.

        Returns:
            read_msg(Any): json-объект уведомления
        """
        with self._con.cursor(row_factory=dict_row) as cur:
            sql = """
                SELECT notification FROM notify_schedule.personal LIMIT 1;
            """
            cur.execute(sql)
            read_msg = cur.fetchone()
            if read_msg is not None:
                return read_msg["notification"]
        return None


@lru_cache()
def get_postgres() -> Postgres:
    """Фабрика для получения экземпляра класса Postgres.

    Returns:
        Postgres(Postgres): экземпляр для работы с Postgres
    """
    return Postgres(get_postgres_con())
