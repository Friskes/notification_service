from __future__ import annotations

import asyncio
import logging
log = logging.getLogger(__name__)

from django.db.models import Q
from django.conf import settings

import httpx


async def asave_message(message, status: str):
    """
    Асинхронно сохраняет сообщение с новыми статусом
    """
    message.status = status
    await message.asave()


async def send_mailing_to_client(mailing, client, message, post_headers: dict[str, str]):
    """
    Асинхронно пытается передать сообщение клиенту,
    в случае возникновения проблем с сетью, повторяет попытку, до тех пор,
    пока сообщение не будет доставлено или текущее время не станет больше времени окончания рассылки
    """
    log.info(
        f"Начата отправка сообщения с id: {message.pk}"
        f" для рассылки с id: {mailing.pk} для клиента с id: {client.pk}"
    )

    payload = {
        "id": message.pk,
        "phone": client.phone,
        "text": mailing.text
    }

    while mailing.can_send:
        try:
            async with httpx.AsyncClient() as aclient:

                response = await aclient.post(
                    f"{settings.PROBE_SERVER_URL}{message.pk}",
                    json=payload,
                    headers=post_headers
                )
                log.info(
                    f"Сообщение с id: {message.pk} для рассылки с id: {mailing.pk} для клиента с id: {client.pk}"
                    f" было отправлено на удаленный сервер, статус ответа: {response.status_code}"
                )
                response.raise_for_status()

            await asave_message(message, 'sent')
            log.info(
                f"Сообщение с id: {message.pk} для рассылки с id: {mailing.pk} для клиента с id: {client.pk}"
                " успешно отправлено :) присвоен статус <sent>"
            )
            return

        except (ConnectionError, Exception) as exc:
            log.info(
                f"Сообщение с id: {message.pk} для рассылки с id: {mailing.pk} для клиента с id: {client.pk}"
                f" не получилось отправить изза ошибки: {exc}"
            )

        await asave_message(message, 'failed')
        log.info(
            f"Сообщение с id: {message.pk} для рассылки с id: {mailing.pk} для клиента с id: {client.pk}"
            " не удалось отправить :( присвоен статус <failed>"
        )


async def generate_mailing_tasks(*args, **kwargs):
    """
    Создает асинхронные задачи для рассылки данных всем клиентам подходящим под фильтр.
    """
    from notification.models import Mailing, Client, Message

    post_headers = {
        'Authorization': f'Bearer {settings.PROBE_SERVER_TOKEN}',
        'Content-Type': 'application/json'
    }

    mailing = await Mailing.objects.aget(id=kwargs['mailing_id'])

    tasks = []
    async for client in Client.objects.filter(
        Q(code__in=mailing.mobile_codes) | Q(tag__in=mailing.tags)
    ):
        message = await Message.objects.acreate(
            status='proceeded',
            mailing=mailing,
            client=client
        )
        log.info(
            f"Сообщение с id: {message.pk} для рассылки с id: {mailing.pk} для клиента с id: {client.pk}"
            " успешно создано, присвоен статус <proceeded>"
        )

        task = asyncio.create_task(send_mailing_to_client(mailing, client, message, post_headers))
        tasks.append(task)

    await asyncio.gather(*tasks)
