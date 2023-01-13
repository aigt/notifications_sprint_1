from functools import lru_cache
from typing import Optional

from psycopg import Connection

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

    def read_notifications(self):
        with self._con.cursor() as cur:
            sql = """
                SELECT * FROM notify_schedule.personal;
            """
            cur.execute(sql)
            result = cur.fetchall()
        return f"THE TEST RESULT IS {result}"

        # self._con.commit()

@lru_cache()
def get_postgres() -> Postgres:
    """Фабрика для получения экземпляра класса Postgres.

    Returns:
        Postgres(Postgres): экземпляр для работы с Postgres
    """
    return Postgres(get_postgres_con())
