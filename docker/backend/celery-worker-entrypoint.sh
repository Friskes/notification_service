#!/usr/bin/env bash

echo ">>> EXECUTION CELERY-WORKER-ENTRYPOINT.SH"

mkdir -p /var/run/celery /var/log/celery
chown -R nobody:nogroup /var/run/celery /var/log/celery

python manage.py runcelery "celery --app=${CELERY_APP} worker -E \
--statedb=/var/run/celery/worker-example@%h.state \
--hostname=worker-example@%h --uid=nobody --gid=nogroup \
--loglevel=INFO \
--logfile=/var/log/celery/worker-example.log"
# Если указать лог файл для Celery то лог (stdout, stderr) будет перенаправлен из консоли в файл

# https://testdriven.io/courses/django-celery/auto-reload/#H-4-solution-2-watchfiles
# pip install watchfiles
# watchfiles --filter python \
#             "celery --app=${CELERY_APP} worker -E \
#             --statedb=/var/run/celery/worker-example@%h.state \
#             --hostname=worker-example@%h \
#             --uid=nobody --gid=nogroup \
#             --loglevel=INFO"
#             # --queues=celery.example -O fair # изза этого параметра селери не извлекает сообщения из очереди
#             # --logfile=/var/log/celery/worker-example.log
#             # Если указать лог файл для Celery то лог (stdout, stderr) будет перенаправлен из консоли в файл

# https://github.com/celery/celery/issues/3759
# https://docs.celeryq.dev/en/latest/userguide/workers.html#variables-in-file-paths
# https://stackoverflow.com/a/59659476/19276507
# exec celery --app=${CELERY_APP} worker -E \
#             --statedb=/var/run/celery/worker-example@%h.state \
#             --hostname=worker-example@%h \
#             --uid=nobody --gid=nogroup \
#             --loglevel=INFO
#             # --queues=celery.example -O fair # изза этого параметра селери не извлекает сообщения из очереди
#             # --logfile=/var/log/celery/worker-example.log
#             # Если указать лог файл для Celery то лог (stdout, stderr) будет перенаправлен из консоли в файл
