import pytest
from settings import Settings, get_settings

pytest_plugins = (
    "fixtures.rabbitmq",
    "fixtures.templates_db",
    "fixtures.history_db",
)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()
