import logging
from time import sleep

from core import logger


def main() -> None:
    """Точка входа в приложение тест."""
    logger.configure_logging()
    while True:
        logging.info("Hellow from worker")
        sleep(15)  # noqa: WPS432


if __name__ == "__main__":
    main()
