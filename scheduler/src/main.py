import pika

from core.settings import get_settings
from core.start_up import start_up

settings = get_settings()


def publish(channel, exchange, queue, body):
    channel.basic_publish(exchange=exchange,
                          routing_key=queue,
                          body=body)

def callback(ch, method, properties, body):
    print(f'Message recieved: {body}')

def read(channel, queue, fn):
    channel.basic_consume(queue=queue,
                          auto_ack=True,
                          on_message_callback=fn)
    channel.start_consuming()


if __name__ == "__main__":
    start_up()

    # credentials = pika.PlainCredentials('user', 'pass')
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
    #                                                                port=5672,
    #                                                                credentials=credentials))
    #
    # channel = connection.channel()
    #
    # publish(channel=channel,
    #         exchange=settings.rb_exchange,
    #         queue=settings.rb_transfer_queue,
    #         body="Hello, World!"
    #         )
    # read(channel=channel,
    #      queue=settings.rb_transfer_queue,
    #      fn=callback)

