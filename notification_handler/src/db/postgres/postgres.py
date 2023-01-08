from functools import lru_cache
from typing import Optional

from psycopg import Connection

from db.base import BaseDatabase
from models.notification import Notification

postgres_con: Optional[Connection] = None


@lru_cache
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

    def add_notification(self, table: str, notification: Notification) -> None:
        """Добавление данных в таблицу info.

        Args:
            table(str): Имя таблицы
            notification(Notification): Данные для добавления в таблицу
        """


@lru_cache()
def get_postgres() -> Postgres:
    """Фабрика для получения экземпляра класса Postgres.

    Returns:
        Postgres(Postgres): экземпляр для работы с Postgres
    """
    return Postgres(get_postgres_con())
