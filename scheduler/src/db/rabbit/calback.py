def callback(ch, method, properties, body):
    print(f'Message recieved: {body}')