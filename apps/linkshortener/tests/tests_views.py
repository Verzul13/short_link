from django.test import TestCase

from rest_framework.test import APIClient

from ..models import ShortLink


class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.short_link_test = ShortLink.objects.create(
            long_url='http://test_one.ru',
            subpart='ZXCVBN'
        )

    def test_redirect_subpart_db_ok(self):
        # Отправляем get запрос с subpart, который есть в БД, получаем 302(редирект)

        response = self.client.get(f"http://testserver/ZXCVBN",
                                   catch_response=True,
                                   )

        self.assertEqual(response.status_code, 302)

    def test_redirect_subpart_db_no_ok(self):
        # Отправляем get запрос с subpart, которого нет в БД, получаем 404

        response = self.client.get(f"http://testserver/XXXXXX",
                                   catch_response=True,
                                   )

        self.assertEqual(response.status_code, 404)
