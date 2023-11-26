# Сервис уведомлений
Сервис управления рассылками API администрирования и получения статистики.

#### Задание https://vans-tan-09u.craft.me/n6OVYFVUpq0o6L

## 1. Зависимости
Для запуска этого проекта потребуется:
- Git
- Docker

## 2. Установка
Создайте .env файл в корне проекта с содержимым:
```shell script
PROBE_SERVER_URL=https://probe.fbrq.cloud/v1/send/
PROBE_SERVER_TOKEN=<секретный JWT токен>

RUN_DEV_SERVER_WITH_DOCKER=1

POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

RABBITMQ_DEFAULT_USER=RABBITMQ_DEFAULT_USER
RABBITMQ_DEFAULT_PASS=RABBITMQ_DEFAULT_PASS
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672

CELERY_APP=config
CELERY_FLOWER_URL_PREFIX=flower
CELERY_FLOWER_ADDRESS=celery-flower
CELERY_FLOWER_PORT=5555
```

Выполните команды:
```shell script
# клонирование удаленного репозитория
git clone https://gitlab.com/Friskes/notification_service.git
# создание образа и запуск контейнеров
docker compose up --build -d
# создание суперпользователя для входа в админку
docker exec -it wsgiserver python manage.py createsuperuser
# остановка контейнеров
docker compose down
```

Адрес документации к API:
```
http://127.0.0.1:8000/docs/
```

### Выполненые дополнительные задания:
3. подготовить docker-compose для запуска всех сервисов проекта одной командой

5. сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: https://petstore.swagger.io

9. удаленный сервис может быть недоступен, долго отвечать на запросы или выдавать некорректные ответы. Необходимо организовать обработку ошибок и откладывание запросов при неуспехе для последующей повторной отправки. Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок.

12. обеспечить подробное логирование на всех этапах обработки запросов, чтобы при эксплуатации была возможность найти в логах всю информацию по
• id рассылки - все логи по конкретной рассылке (и запросы на api и внешние запросы на отправку конкретных сообщений)
• id сообщения - по конкретному сообщению (все запросы и ответы от внешнего сервиса, вся обработка конкретного сообщения)
• id клиента - любые операции, которые связаны с конкретным клиентом (добавление/редактирование/отправка сообщения/…)

### Полезное
```
https://stackoverflow.com/questions/71081084/modern-best-approach-to-using-django-orm-with-async
https://stackoverflow.com/questions/74737310/sync-to-async-django-orm-queryset-foreign-key-property
https://stackoverflow.com/questions/5445174/or-operator-in-django-model-queries
https://stackoverflow.com/a/36257323/19276507
```
