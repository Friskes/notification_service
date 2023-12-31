import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


RUN_DEV_SERVER_WITH_DOCKER = bool(int(os.environ.get('RUN_DEV_SERVER_WITH_DOCKER', '0')))
WINDOWS_POSTGRES_INSTALLED = bool(int(os.environ.get('WINDOWS_POSTGRES_INSTALLED', '1')))

PROBE_SERVER_URL = os.getenv("PROBE_SERVER_URL")
PROBE_SERVER_TOKEN = os.getenv("PROBE_SERVER_TOKEN")

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST') if RUN_DEV_SERVER_WITH_DOCKER else '127.0.0.1'
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

REDIS_HOST = os.environ.get('REDIS_HOST') if RUN_DEV_SERVER_WITH_DOCKER else '127.0.0.1'
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_URL_DB_0 = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
REDIS_URL_DB_1 = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'

RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST') if RUN_DEV_SERVER_WITH_DOCKER else 'localhost'
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')
RABBITMQ_URL = f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'

CELERY_APP = os.environ.get('CELERY_APP')
CELERY_FLOWER_URL_PREFIX = os.environ.get('CELERY_FLOWER_URL_PREFIX', 'flower')
CELERY_FLOWER_ADDRESS = os.environ.get('CELERY_FLOWER_ADDRESS') if RUN_DEV_SERVER_WITH_DOCKER else '127.0.0.1'
CELERY_FLOWER_PORT = os.environ.get('CELERY_FLOWER_PORT', '5555')
