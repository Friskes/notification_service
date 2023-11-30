import logging
log = logging.getLogger(__name__)

from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from notification.services import service


class Mailing(models.Model):
    """
    Модель рассылки
    """
    text = models.TextField("Текст сообщения для доставки клиенту")

    beginning = models.DateTimeField("Дата и время запуска рассылки")

    ending = models.DateTimeField("Дата и время окончания рассылки")

    mobile_codes = ArrayField(
        models.PositiveSmallIntegerField(
            "Фильтр свойств клиентов, на которых должна быть произведена рассылка - код мобильного оператора",
            blank=True,
            validators=[
                MinValueValidator(301), MaxValueValidator(999)
            ]
        ),
        size=5, # макс количество итемов в списке
        verbose_name="Список кодов мобильных операторов"
    )
    tags = ArrayField(
        models.CharField(
            "Фильтр свойств клиентов, на которых должна быть произведена рассылка - тег",
            max_length=50,
            blank=True
        ),
        size=5,
        verbose_name="Массив произвольных тегов"
    )

    @property
    def get_sent_messages(self):
        """
        Возвращает количество сообщений связанных с текущей рассылкой со статусом "sent"
        """
        return len(self.messages.filter(status=self.messages.model.SENT))

    @property
    def get_messages_to_send(self):
        """
        Возвращает количество сообщений связанных с текущей рассылкой со статусом "proceeded"
        """
        return len(self.messages.filter(status=self.messages.model.PROCEEDED))

    @property
    def get_unsent_messages(self):
        """
        Возвращает количество сообщений связанных с текущей рассылкой со статусом "failed"
        """
        return len(self.messages.filter(status=self.messages.model.FAILED))

    @property
    def can_send(self):
        """
        Возвращает истину если текущее время меньше времени окончания рассылки иначе возвращает ложь
        """
        return timezone.now() < self.ending

    def save(self, *args, **kwargs):
        creating = not bool(self.pk)
        result = super().save(*args, **kwargs)

        service.create_mailing_task(self, creating)
        return result

    def __str__(self):
        return f"Рассылка с id: {self.pk} с временем начала: {self.beginning}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Client(models.Model):
    """
    Модель клиента
    """
    phone = models.PositiveBigIntegerField(
        "Номер телефона клиента",
        unique=True,
        validators=[
            MaxValueValidator(79999999999),
            RegexValidator(
                regex=r"^7\w{10}$",
                message="Номер телефона клиента должен быть в формате 7XXXXXXXXXX (X - цифра от 0 до 9)"
            )
        ]
    )
    code = models.PositiveSmallIntegerField(
        "Код мобильного оператора",
        validators=[
            MinValueValidator(301), MaxValueValidator(999) # диапазон кодов в рф
        ]
    )

    tag = models.CharField("Тег (произвольная метка)", max_length=50)

    time_zone = models.CharField("Часовой пояс", max_length=50)

    def __str__(self):
        return f"Клиент с id: {self.pk} с номером: {self.phone}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    """
    Модель сообщения
    """
    SENT = "sent"
    PROCEEDED = "proceeded"
    FAILED = "failed"

    STATUS_CHOICES = [
        (SENT, SENT.title()),
        (PROCEEDED, PROCEEDED.title()),
        (FAILED, FAILED.title()),
    ]

    date = models.DateTimeField("Дата и время создания (отправки)", auto_now_add=True)

    status = models.CharField("Статус отправки", max_length=9, choices=STATUS_CHOICES)

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="messages")

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return f"Сообщение с id: {self.pk} для рассылки с id: {self.mailing.pk} для клиента с id: {self.client.pk}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
