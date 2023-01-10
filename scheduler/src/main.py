import pika


def publish(channel, queue):
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body='Hello World!')

def callback(ch, method, properties, body):
    print(f'Messagerecieved: {body}')

def read(channel, queue, fn):
    channel.basic_consume(queue=queue,
                          auto_ack=True,
                          on_message_callback=fn)
    channel.start_consuming()


if __name__ == "__main__":
    credentials = pika.PlainCredentials('user', 'pass')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                   port=5672,
                                                                   credentials=credentials))

    channel = connection.channel()

    publish(channel, 'worker')
    read(channel, 'worker', callback)

