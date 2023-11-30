from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from notification.services import service
from notification.serializers import ClientSerializer, MessageSerializer, MailingSerializer
from notification.models import Client, Mailing, Message


class ClientViewSet(viewsets.ModelViewSet):
    """
    Определяет эндпоинты для
    получения всех/одного,
    создания,
    полного/частичного изменения,
    удаления клиентов.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        tags=['Получение клиентов'],
        operation_id='Получить список всех клиентов',
        operation_description='Получить список всех клиентов'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Получение клиентов'],
        operation_id='Получить клиента по ID',
        operation_description='Получить клиента по ID'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение клиента'],
        operation_id='Создать клиента',
        operation_description='Создать клиента'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение клиента'],
        operation_id='Изменить клиента полностью по ID',
        operation_description='Изменить клиента полностью по ID'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение клиента'],
        operation_id='Изменить клиента частично по ID',
        operation_description='Изменить клиента частично по ID'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Удаление клиента'],
        operation_id='Удалить клиента по ID',
        operation_description='Удалить клиента по ID'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MailingViewSet(viewsets.ModelViewSet):
    """
    Определяет эндпоинты для
    получения статистики и
    получения всех/одного,
    создания,
    полного/частичного изменения,
    удаления рассылок.
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @swagger_auto_schema(
        tags=['Получение статистики рассылок'],
        operation_id='Получить список статистики по всем рассылкам',
        operation_description='Получить список статистики по всем рассылкам'
    )
    @action(["get"], False)
    def fullstat(self, request):
        statistics = service.get_statistics(
            self.queryset
        )
        return Response(statistics)

    @swagger_auto_schema(
        tags=['Получение статистики рассылок'],
        operation_id='Получить статистику рассылки по ID',
        operation_description='Получить статистику рассылки по ID'
    )
    @action(["get"], True)
    def stat(self, request, pk=None):
        statistics = service.get_statistics(
            get_list_or_404(self.queryset, pk=pk)
        )
        return Response(statistics)

    @swagger_auto_schema(
        tags=['Получение рассылок'],
        operation_id='Получить список всех рассылок',
        operation_description='Получить список всех рассылок'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Получение рассылок'],
        operation_id='Получить рассылку по ID',
        operation_description='Получить рассылку по ID'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение рассылки'],
        operation_id='Создать рассылку',
        operation_description='Создать рассылку'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение рассылки'],
        operation_id='Изменить рассылку полностью по ID',
        operation_description='Изменить рассылку полностью по ID'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение рассылки'],
        operation_id='Изменить рассылку частично по ID',
        operation_description='Изменить рассылку частично по ID'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Удаление рассылки'],
        operation_id='Удалить рассылку по ID',
        operation_description='Удалить рассылку по ID'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    """
    Определяет эндпоинты для
    получения всех/одного,
    создания,
    полного/частичного изменения,
    удаления сообщений.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @swagger_auto_schema(
        tags=['Получение сообщений'],
        operation_id='Получить список всех сообщений',
        operation_description='Получить список всех сообщений'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Получение сообщений'],
        operation_id='Получить сообщение по ID',
        operation_description='Получить сообщение по ID'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение сообщения'],
        operation_id='Создать сообщение',
        operation_description='Создать сообщение'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение сообщения'],
        operation_id='Изменить сообщение полностью по ID',
        operation_description='Изменить сообщение полностью по ID'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Создание / Изменение сообщения'],
        operation_id='Изменить сообщение частично по ID',
        operation_description='Изменить сообщение частично по ID'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Удаление сообщения'],
        operation_id='Удалить сообщение по ID',
        operation_description='Удалить сообщение по ID'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
