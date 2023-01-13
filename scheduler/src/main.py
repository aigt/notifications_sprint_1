import time

from core.settings import get_settings
from core.start_up import start_up
from db.postgres.postgres import get_postgres
from db.rabbit.rabbitmq import get_rabbit

settings = get_settings()


def main() -> None:
    start_up()
    rabbit = get_rabbit()
    postgres = get_postgres()
    while True:
        recieved_msg = postgres.read_notifications()
        print(recieved_msg)
        rabbit.send("generator", recieved_msg)
        time.sleep(5)


if __name__ == "__main__":
    time.sleep(10)
    main()
