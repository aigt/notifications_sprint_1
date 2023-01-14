from typing import Any, Generator, List, Optional

from psycopg import Connection, sql

from db.base import BaseDatabase

postgres_con: Optional[Connection] = None


def get_postgres_con() -> Connection:
    """Фабрика для получения соединения с postgres.

    Returns:
        postgres_con(Connection): соединение с postgres
    """
    return postgres_con


class Postgres(BaseDatabase):
    """Класс для работы с Postgres."""

    fetchmany_size = 7777

    def __init__(self, connect: Connection):
        self._con = connect

    def get_users_emails(self, user_id_list: List[str]) -> Any:
        """Запрос списка почты пользователей.

        Args:
            user_id_list(list): Список пользователей

        Returns:
            (list): Список пар {user_id: email}
        """
        with self._con.cursor() as cur:
            query = sql.SQL(
                """
            SELECT email, user_id
            FROM users_auth.users_data
            where user_id IN ({0})
            """,
            ).format(sql.SQL(",").join(user_id_list))
            cur.execute(query)
            return cur.fetchall()

    def get_emails_all_users(self) -> Generator:
        """Генератор для получения списка почты всех пользователей.

        Yields:
            emails(list): Список словарей {user_id: email}
        """
        with self._con.cursor() as cur:
            query = """
            SELECT email, user_id
            FROM users_auth.users_data
            """
            cur.execute(query)
            while emails := cur.fetchmany(self.fetchmany_size):
                yield emails


def get_postgres() -> Postgres:
    """Фабрика для получения экземпляра класса Postgres.

    Returns:
        Postgres(Postgres): экземпляр для работы с Postgres
    """
    return Postgres(get_postgres_con())
