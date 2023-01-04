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
