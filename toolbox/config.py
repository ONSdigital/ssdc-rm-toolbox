import os


class Config:
    SERVICE_NAME = os.getenv('SERVICE_NAME', 'ssdc-rm-toolbox')

    EVENT_SCHEMA_VERSION = 'v0.3_RELEASE'
    EVENT_CHANNEL = os.getenv('EVENT_CHANNEL', 'RM')
    SHARED_PUBSUB_PROJECT = os.getenv('SHARED_PUBSUB_PROJECT', 'shared-project')
    NEW_CASE_TOPIC = os.getenv('NEW_CASE_TOPIC', 'event_new-case')
    EXCEPTIONMANAGER_HOST = os.getenv('EXCEPTIONMANAGER_HOST', 'localhost')
    EXCEPTIONMANAGER_PORT = os.getenv('EXCEPTIONMANAGER_PORT', '8666')
    EXCEPTIONMANAGER_URL = f'http://{EXCEPTIONMANAGER_HOST}:{EXCEPTIONMANAGER_PORT}'

    BAD_MESSAGE_MINIMUM_SEEN_COUNT = os.getenv('BAD_MESSAGE_MINIMUM_SEEN_COUNT', '4')

    CURRENT_USER = os.getenv('CURRENT_USER', 'anonymous')
