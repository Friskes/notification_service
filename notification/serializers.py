from rest_framework import serializers

from notification.models import Client, Message, Mailing


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериализует данные клиента
    """
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализует данные сообщения
    """
    class Meta:
        model = Message
        fields = "__all__"


class MailingSerializer(serializers.ModelSerializer):
    """
    Сериализует данные рассылки
    """
    class Meta:
        model = Mailing
        fields = "__all__"
