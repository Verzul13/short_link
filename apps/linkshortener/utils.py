import string
import random

from django.contrib.sites.shortcuts import get_current_site

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import ShortLink


def ValidationError(error: str):  # noqa
    return Response(data={"error": [error]},
                    status=status.HTTP_400_BAD_REQUEST)


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # Создает строку с рандомными англ.буквами и цифрами в верхнем регистре
    while True:
        subpart = ''.join(random.choice(chars) for _ in range(size))
        short_link = ShortLink.objects.filter(subpart=subpart).first()
        if not short_link:
            break
    return subpart


def create_full_url(request: Request, subpart: str) -> str:
    # Возвращает полный url ссылки
    current_site = get_current_site(request)
    full_url = f'http://{current_site}/{subpart}'

    return full_url
