import json

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from ..models import ShortLink


class TestCreateShortLink(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.short_link_test = ShortLink.objects.create(
            long_url='http://test_one.ru',
            subpart='ZXCVBN'
        )

    def test_create_short_link_200(self):
        # создание ShortLink
        data = {
            'link': 'http://test.ru'
        }
        response = self.client.post(reverse('linkshortener:short_link-list'), data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        short_link = ShortLink.objects.filter(long_url='http://test.ru').first()
        response_data = {
            'old_url': short_link.long_url,
            'subpart': short_link.subpart,
            'full_url': f'http://testserver/{short_link.subpart}'
        }
        self.assertEqual(response.json(), response_data)

    def test_create_short_link_custom_subpart_200(self):
        # создание ShortLink с кастомным subpart
        data = {
            'link': 'http://test.ru',
            'subpart': 'QWERTY'
        }
        response = self.client.post(reverse('linkshortener:short_link-list'), data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        short_link = ShortLink.objects.filter(long_url='http://test.ru').first()
        response_data = {
            'old_url': short_link.long_url,
            'subpart': 'QWERTY',
            'full_url': 'http://testserver/QWERTY'
        }
        self.assertEqual(response.json(), response_data)

    def test_create_short_link_incorrect_link(self):
        # error некорректный url
        data = {
            'link': 'test.ru'
        }
        response = self.client.post(reverse('linkshortener:short_link-list'), data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_short_link_incorrect_subpart(self):
        # error некорректный subpart
        data = {
            'link': 'http://test.ru',
            'subpart': 'ZXCVB'
        }
        response = self.client.post(reverse('linkshortener:short_link-list'), data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_short_link_short_already(self):
        # error subpart уже используется
        data = {
            'link': 'http://test.ru',
            'subpart': 'ZXCVBN'
        }
        response = self.client.post(reverse('linkshortener:short_link-list'), data=json.dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)


class TestGetListShortLink(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.short_link_test_1 = ShortLink.objects.create(
            long_url='http://test_one.ru',
            subpart='ZXCVBN'
        )
        self.short_link_test_2 = ShortLink.objects.create(
            long_url='http://test_two.ru',
            subpart='QWERTY'
        )

    def test_get_list_hort_links(self):
        # Получаем список ShortLink c колличеством, пагинацией и сортировкой по дате создания
        response = self.client.get(reverse('linkshortener:short_link-list'),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_data = {
            'count': 2,
            'links': [
                {
                    'full_url': f'http://testserver/{self.short_link_test_2.subpart}',
                    'visit': None,
                    'long_url': self.short_link_test_2.long_url,
                    'subpart': self.short_link_test_2.subpart

                },
                {
                    'full_url': f'http://testserver/{self.short_link_test_1.subpart}',
                    'visit': None,
                    'long_url': self.short_link_test_1.long_url,
                    'subpart': self.short_link_test_1.subpart
                }
            ]
        }

        self.assertEqual(response.json(), response_data)
