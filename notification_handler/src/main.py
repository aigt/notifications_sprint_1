from core.add_queue import add_queue
from core.start_up import start_up  # type: ignore

from db.rabbit.callback import callback
from db.rabbit.rabbitmq import get_rabbit


def main() -> None:
    """Точка входа в приложение."""
    start_up()
    add_queue()
    rabbit = get_rabbit()
    rabbit.start_consume(callback)


if __name__ == "__main__":
    main()
