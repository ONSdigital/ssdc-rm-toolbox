import os


class Config:
    NAME = 'ssdc-rm-toolbox'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%Y-%m-%dT%H:%M:%S.%f')
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_HTTP_PORT = os.getenv('RABBITMQ_HTTP_PORT', '16672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    EXCEPTIONMANAGER_HOST = os.getenv('EXCEPTIONMANAGER_HOST', 'localhost')
    EXCEPTIONMANAGER_PORT = os.getenv('EXCEPTIONMANAGER_PORT', '8666')
    EXCEPTIONMANAGER_URL = f'http://{EXCEPTIONMANAGER_HOST}:{EXCEPTIONMANAGER_PORT}'
    QID_MODULUS = os.getenv('QID_MODULUS', '1')
    QID_FACTOR = os.getenv('QID_FACTOR', '1')

    ENVIRONMENT = os.getenv('ENVIRONMENT')
    LOG_LEVEL_PIKA = os.getenv('LOG_LEVEL_PIKA', 'ERROR')

    BAD_MESSAGE_MINIMUM_SEEN_COUNT = os.getenv('BAD_MESSAGE_MINIMUM_SEEN_COUNT', '4')
