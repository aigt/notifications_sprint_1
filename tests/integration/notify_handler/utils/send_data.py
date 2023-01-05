from pika.adapters.blocking_connection import BlockingChannel


def send(channel: BlockingChannel, queue: str, data_for_send: str) -> None:
    """Отправка данных в очередь.

    Args:
        channel(BlockingChannel): канал RabbirMQ
        queue(str): Название очереди
        data_for_send(str): Данные для отправки
    """
    channel.basic_publish(exchange="", routing_key=queue, body=data_for_send)
