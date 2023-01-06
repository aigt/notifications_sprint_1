from typing import Optional

from psycopg import Connection

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

    def __init__(self, connect: Connection):
        self._con = connect

    def get_user_name(self, email: str) -> None:
        """Запрос имени пользователя по его почте.

        Args:
            email(str): Почта
        """


def get_postgres() -> Postgres:
    """Фабрика для получения экземпляра класса Postgres.

    Returns:
        Postgres(Postgres): экземпляр для работы с Postgres
    """
    return Postgres(get_postgres_con())
