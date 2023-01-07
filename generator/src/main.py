from core.add_queue import add_queue
from core.logger import configure_logging
from core.start_up import start_up
from db.rabbit.callback import callback
from db.rabbit.rabbitmq import get_rabbit

configure_logging()


def main() -> None:
    """Точка входа в приложение.

    В начале создаются все подключения, после запускается ожидание уведомлений из очереди.
    """
    start_up()
    add_queue()
    rabbit = get_rabbit()
    rabbit.start_consume(callback)


if __name__ == "__main__":
    main()
