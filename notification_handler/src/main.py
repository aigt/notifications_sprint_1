import logging

from core.start_up import start_up  # type: ignore
from db.rabbit.callback import callback
from db.rabbit.rabbitmq import get_rabbit

from core.logger import configure_logging
from core.settings import get_settings
from core.add_queue import add_queue

settings = get_settings()
configure_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    """Точка входа в приложение."""
    add_queue()
    rabbit = get_rabbit()
    rabbit.start_consume(callback)


if __name__ == "__main__":
    start_up()
    main()
