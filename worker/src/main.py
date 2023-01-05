import logging

from core import builder, logger


def main() -> None:
    """Точка входа в приложение."""
    logging.info("Starting worker")
    logger.configure_logging()
    app = builder.build()
    app.run()


if __name__ == "__main__":
    main()
