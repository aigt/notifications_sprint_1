from typing import Generator

import psycopg
from psycopg import Cursor
from psycopg.rows import dict_row
from pytest import fixture
from settings import get_settings
from utils.add_postgres_data import add_users

settings = get_settings()


@fixture(scope="function")
def postgres_cur() -> Generator:
    """postgres курсор."""
    con = psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.users_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        row_factory=dict_row,
    )
    cur = con.cursor()
    yield cur
    con.close()


@fixture(scope="function")
def add_users_postgres(postgres_cur: Cursor) -> Generator:
    """Фикстура для загрузки и очистки данных из коллекции bookmark."""
    add_users(postgres_cur)
    yield
    postgres_cur.execute("DELETE FROM users_auth.users_data")
    postgres_cur.execute("DELETE FROM users_auth.users")
    postgres_cur.connection.commit()
