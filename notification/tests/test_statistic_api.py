from datetime import timedelta
import json

from django.urls import reverse
from django.utils import timezone

from rest_framework import test, status

from notification.serializers import MailingSerializer, ClientSerializer, MessageSerializer
from notification.models import Mailing, Client, Message


# docker exec -it wsgiserver python manage.py test notification.tests.test_statistic_api
# docker exec -it wsgiserver python manage.py test notification.tests.test_statistic_api.StatisticAPITestCase
# для работы тестов вне docker необходимо заранее поднять celery в отдельном терминале командой: python manage.py runcelery -b -f
# python manage.py test notification.tests.test_statistic_api --verbosity 2
# python manage.py test notification.tests.test_statistic_api.StatisticAPITestCase
class StatisticAPITestCase(test.APITestCase):
    """
    """
    # def setUp(self):
    #     Client.objects.create(phone=79896349874, code=989, tag='mytag', time_zone='Europe/Moscow')
    #     Client.objects.create(phone=79894249864, code=989, tag='mytag', time_zone='Europe/Moscow')
    #     Client.objects.create(phone=79899269721, code=989, tag='mytag', time_zone='Europe/Moscow')

    #     Mailing.objects.create(
    #         text='text1',
    #         beginning=timezone.now(),
    #         ending=timezone.now() + timedelta(minutes=1),
    #         mobile_codes=[989, 999],
    #         tags=['mytag', 'mytag2']
    #     )
    #     Mailing.objects.create(
    #         text='text2',
    #         beginning=timezone.now(),
    #         ending=timezone.now() + timedelta(minutes=1),
    #         mobile_codes=[989, 999],
    #         tags=['mytag', 'mytag2']
    #     )
    #     Mailing.objects.create(
    #         text='text3',
    #         beginning=timezone.now(),
    #         ending=timezone.now() + timedelta(minutes=1),
    #         mobile_codes=[989, 999],
    #         tags=['mytag', 'mytag2']
    #     )

    def test_get(self):
        #                            class_name-method_name
        mailing_fullstat_url = reverse('mailing-fullstat')
        response = self.client.get(mailing_fullstat_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        mailing_list_url = reverse('mailing-list')
        beginning = timezone.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        ending = (timezone.now() + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        request_data = json.dumps({
            "text": "string",
            "beginning": beginning,
            "ending": ending,
            "mobile_codes": [
                999
            ],
            "tags": [
                "string"
            ]
        })
        response = self.client.post(mailing_list_url, data=request_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mailing = Mailing.objects.get(id=1)
        mailing_serializer = MailingSerializer(mailing)
        self.assertEqual(response.data, mailing_serializer.data)
