import logging
import string
import random

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from drf_yasg.utils import swagger_auto_schema

from linkshortener.tasks import write_redis_and_create_visit
from .swagger_schema import CREATE_SHORT_LINK_RESPONSE, LIST_SHORT_LINK_PARAMETER
from .models import ShortLink
from .serializers import ShortLinkCreateSerializer, ShortLinkSerializer
from .utils import ValidationError


logger = logging.getLogger("short_link")


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
        записывает его значение в кэш и создает запись в LinkVisit
        '''
        serializer = ShortLinkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subpart = random_generator()
        if serializer.validated_data.get('subpart'):
            subpart = serializer.validated_data.get('subpart')

        short_link = ShortLink.objects.filter(subpart=subpart).first()
        if short_link:
            return ValidationError('This short link is already in the database')
        try:
            short_link = ShortLink.objects.create(
                long_url=serializer.validated_data['long_url'],
                subpart=subpart
            )
        except Exception as e:
            logger.error(f'Error when creating short_link: {e}')
            return ValidationError('Error when creating short_link')

        write_redis_and_create_visit.delay(short_link.id, subpart, serializer.validated_data['long_url'])
        logger.error(f'Succes when creating short_link: {short_link}')

        data = {
            "id": short_link.id,
            "subpart": subpart
        }
        return Response(data, status=HTTP_200_OK)

    @swagger_auto_schema(**LIST_SHORT_LINK_PARAMETER, tags=["app"])
    def list(self, request) -> Response:
        '''
        Возвращает список ShortLinks с пагинацией
        '''
        params = request.query_params
        page = int(params.get("page", "1"))
        limit = int(params.get("limit", "10"))
        data = self.queryset[(page - 1)*limit: page * limit]
        short_links = self.get_serializer(data, many=True).data

        return Response(short_links)


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
