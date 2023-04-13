import os

RABBIT_MQ_USER = os.environ.get('RABBIT_MQ_USER', 'todo')
RABBIT_MQ_PASSWORD = os.environ.get('RABBIT_MQ_PASSWORD', 'T7sd78sVai3jDNs')
RABBIT_MQ_HOST = os.environ.get('RABBIT_MQ_HOST', 'localhost')
RABBIT_MQ_PORT = os.environ.get('RABBIT_MQ_PORT', 5672)

BROKER_URL = '{protocol}://{user}:{password}@{host}:{port}/'.format(
    protocol='amqp',
    user=RABBIT_MQ_USER,
    password=RABBIT_MQ_PASSWORD,
    host=RABBIT_MQ_HOST,
    port=RABBIT_MQ_PORT,
)
