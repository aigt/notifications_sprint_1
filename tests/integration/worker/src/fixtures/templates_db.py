from typing import Generator

import psycopg
import pytest
from psycopg.rows import dict_row
from pytest import fixture
from settings import Settings
from utils import loaq_query


@fixture(scope="function")
def templates_db(settings: Settings) -> Generator:
    """postgres курсор."""
    with psycopg.connect(conninfo=settings.templates_dsn, row_factory=dict_row) as conn:
        query = loaq_query.load_sql("testdata/templates_db.sql")

        with conn.cursor() as cur_init:
            cur_init.execute(query=query)
            conn.commit()

        yield
