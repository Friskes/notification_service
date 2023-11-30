from sys import argv as django_cmd_argv
from pathlib import Path
from config.env import *


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


if RUN_DEV_SERVER_WITH_DOCKER:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL_DB_1,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }


if RUN_DEV_SERVER_WITH_DOCKER or WINDOWS_POSTGRES_INSTALLED:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_DB,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': POSTGRES_HOST,
            'PORT': POSTGRES_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            "TEST": { # отдельная БД для тестов
                "NAME": BASE_DIR / "test_db.sqlite3",
            },
        }
    }


# для выполнения команды python manage.py collectstatic (без докера)
# необходимо сделать доступным STATIC_ROOT и недоступным STATICFILES_DIRS
if RUN_DEV_SERVER_WITH_DOCKER:
    STATIC_ROOT = BASE_DIR / 'static' # если это запуск докера
else:
    if django_cmd_argv[1] == 'collectstatic': # если это обычный запуск python manage.py collectstatic
        STATIC_ROOT = BASE_DIR / 'static'
    else:
        STATICFILES_DIRS = [BASE_DIR / 'static'] # если это обычный запуск python manage.py runserver
