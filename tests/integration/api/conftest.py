from typing import Generator

import requests  # type: ignore
from pytest import fixture

pytest_plugins = (
    "fixtures.rabbitmq",
    "fixtures.postgres_users",
    "fixtures.mongo",
)


@fixture(scope="function")
def http_con() -> Generator:
    """http клиент"""

    con = requests.Session()
    yield con
    con.close()
