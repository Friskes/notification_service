import asyncio
import logging
log = logging.getLogger(__name__)

from notification.services.send_mailing_service import generate_mailing_tasks
from config.celery import app


@app.task(bind=True)
def create_mailing_task(self, *args, **kwargs):
    """
    Запускает асинхронную рассылку
    """
    log.info(f"Запущена задача с id: {self.request.id} для рассылки с id: {kwargs['mailing_id']}")
    kwargs['task_id'] = self.request.id
    asyncio.run(generate_mailing_tasks(*args, **kwargs))
    log.info(f"Завершена задача с id: {self.request.id} для рассылки с id: {kwargs['mailing_id']}")
