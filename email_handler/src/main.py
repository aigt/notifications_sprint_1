import json
from time import sleep

from core.add_queue import add_queue
from core.logger import configure_logging
from core.config import get_settings
from core.start_up import start_up
import pika

from db.rabbit.callback import callback
from db.rabbit.rabbitmq import get_rabbit
from sender.email_sender import send_message

settings = get_settings()
configure_logging()


def main() -> None:
    """Точка входа в приложение."""

    # add_queue()
    # rabbit = get_rabbit()
    # rabbit.start_consume(callback)

    #send
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rb_host,
            port=settings.rb_port,
            credentials=pika.PlainCredentials(settings.rb_user, settings.rb_password),
        ),
    )
    channel = connection.channel()

    channel.queue_declare(queue='email', durable=True)

    queue_message = {'email': 'a1exitt@yandex.ru', 'content': 'test'}
    channel.basic_publish(exchange='', routing_key='email', body=json.dumps(queue_message))
    print(f" [x] Sent {queue_message}")
    connection.close()

    sleep(1)
    # recipe
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rb_host,
            port=settings.rb_port,
            credentials=pika.PlainCredentials(settings.rb_user, settings.rb_password),
        ),
    )
    channel = connection.channel()

    channel.queue_declare(queue='email', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        import orjson
        notification = orjson.loads(body)
        send_message(
            email=notification.get('email'),
            content=notification.get('content')
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='email', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    start_up()
    main()
