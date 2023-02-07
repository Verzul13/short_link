import logging
import string
import random

from django.contrib.sites.shortcuts import get_current_site
from django.db.models import OuterRef

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from drf_yasg.utils import swagger_auto_schema

from linkshortener.tasks import write_redis_and_create_visit
from .swagger_schema import CREATE_SHORT_LINK_RESPONSE, LIST_SHORT_LINK_PARAMETER
from .models import ShortLink, LinkVisit
from .serializers import ShortLinkCreateSerializer, ShortLinkSerializer
from .utils import ValidationError


logger = logging.getLogger("django")


class ShortLinkView(CreateModelMixin, ListModelMixin, GenericViewSet):

    queryset = ShortLink.objects.all()

    def get_serializer_class(self):
        return ShortLinkSerializer

    @swagger_auto_schema(request_body=ShortLinkCreateSerializer,
                         **CREATE_SHORT_LINK_RESPONSE,
                         tags=["app"])
    def create(self, request) -> Response:
        '''
        Проверяет наличие subpart в БД, если его нет - создает объект ShortLink,
        записывает его значение в кэш, создает запись в LinkVisit,
        создает сессию до закрытия браузера пользователем 
        '''
        serializer = ShortLinkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subpart = random_generator()
        if serializer.validated_data.get('subpart'):
            subpart = serializer.validated_data.get('subpart')

        short_link = ShortLink.objects.filter(subpart=subpart).first()
        if short_link:
            return ValidationError('This short link is already in the database')

        session_key = request.session.session_key
        if not request.session.exists(session_key):
            request.session.create()
            session_key = request.session.session_key

        try:
            short_link = ShortLink.objects.create(
                long_url=serializer.validated_data['link'],
                subpart=subpart,
                session_key=session_key
            )
        except Exception as e:
            logger.error(f'Error when creating short_link: {e}')
            return ValidationError('Error when creating short_link')
        # можно было через сигнал, но считаю лучше через селери, т.к. сигналы сложно отслеживать
        write_redis_and_create_visit.delay(short_link.id, subpart, serializer.validated_data['link'])
        full_url = create_full_url(request, subpart)
        data = {
            "old_url": serializer.validated_data['link'],
            "subpart": subpart,
            "full_url": full_url
        }
        # куки сессии пользователя истекает, когда веб-браузер пользователя закрыт
        request.session.set_expiry(0)
        logger.info(f'Succes when creating short_link: {short_link}')

        return Response(data, status=HTTP_200_OK)

    @swagger_auto_schema(**LIST_SHORT_LINK_PARAMETER, tags=["app"])
    def list(self, request) -> Response:
        '''
        Возвращает список ShortLinks с колличеством переходов
        по ссылке и пагинацией
        '''
        session_key = request.session.session_key
        queryset = self.queryset.filter(session_key=session_key).annotate(
            visit=LinkVisit.objects.filter(short_link_id=OuterRef("id")).values('number_of_visits')
        ).order_by('-created_dt')
        params = request.query_params
        page = int(params.get("page", "1"))
        limit = int(params.get("limit", "10"))
        data = queryset[(page - 1)*limit: page * limit]
        count = self.queryset.count()
        short_links = self.get_serializer(data, many=True, context={'request': request}).data
        data = {'count': count, 'links': short_links}

        return Response(data)


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # Создает строку с рандомными англ.буквами и цифрами в верхнем регистре
    return ''.join(random.choice(chars) for _ in range(size))


def create_full_url(request: Request, subpart: str) -> str:
    # Возвращает полный url ссылки
    current_site = get_current_site(request)
    full_url = f'http://{current_site}/{subpart}'

    return full_url
