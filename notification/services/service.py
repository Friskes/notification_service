from __future__ import annotations

import logging
log = logging.getLogger(__name__)

from notification import tasks


def create_mailing_task(self, creating: bool):
    """
    Создает задачу рассылки (сейчас/в будущем) при создании нового объекта в БД
    если текущее время меньше времени окончания рассылки.
    """
    log.info(f'{creating = } {self.can_send = }')

    if creating and self.can_send:
        task_id = tasks.run_mailing_task.apply_async(
            eta=self.beginning,
            expires=self.ending,
            kwargs={
                "mailing_id": self.pk
            }
        )
        log.info(f"Получена задача с id: {task_id} для рассылки с id: {self.pk}")


def get_statistics(queryset) -> list[dict[str, int]]:
    """
    Возвращает статистику по каждой рассылке из queryset
    """
    statistics = []
    for mail in queryset:
        statistics.append({
            'mailing_id': mail.pk,
            'sent_messages': mail.get_sent_messages,
            'messages_to_send': mail.get_messages_to_send,
            'unsent_messages': mail.get_unsent_messages
        })
    return statistics
