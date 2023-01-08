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

    def add_personal_notification(self, notification: Notification) -> None:
        """Добавление данных в таблицу personal.

        Args:
            notification(Notification): Данные для добавления в таблицу
        """
        with self._con.cursor() as cur:
            sql = """
            INSERT INTO notify_schedule.personal (user_id, notification)
            VALUES (%s, %s)
            """
            cur.execute(
                sql,
                (notification.user_id, notification.json()),
            )

        self._con.commit()

    def add_mass_notification(self, notification: Notification) -> None:
        """Добавление данных в таблицу mass.

        Args:
            notification(Notification): Данные для добавления в таблицу
        """
        with self._con.cursor() as cur:
            sql = """
            INSERT INTO notify_schedule.mass (notification)
            VALUES (%s)
            """
            cur.execute(sql, (notification.json(),))

        self._con.commit()


@lru_cache()
def get_postgres() -> Postgres:
    """Фабрика для получения экземпляра класса Postgres.

    Returns:
        Postgres(Postgres): экземпляр для работы с Postgres
    """
    return Postgres(get_postgres_con())
