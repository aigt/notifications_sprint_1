import logging
import time

from core.logger import configure_logging
from core.settings import get_settings

settings = get_settings()
configure_logging()


def main() -> None:
    """Точка входа в приложение."""
    while True:
        logging.getLogger(__name__).info("Hello i'm Generator")
        time.sleep(10)


if __name__ == "__main__":
    main()
