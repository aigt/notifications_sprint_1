import pika


def publish(channel, queue):
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body='Hello World!')

if __name__ == "__main__":
    credentials = pika.PlainCredentials('user', 'pass')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                   port=5672,
                                                                   credentials=credentials))

    channel = connection.channel()

    publish(channel, 'worker')
