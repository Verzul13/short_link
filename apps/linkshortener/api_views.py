from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema

from linkshortener.tasks import test_task
from .swagger_schema import TEST_RESPONSE


@swagger_auto_schema(responses=TEST_RESPONSE, method='GET')
@api_view(['GET'], )
def test(request) -> Response:
    data = {
        'test': 'test'
    }
    test_task.delay()
    return Response(data=data, status=HTTP_200_OK)
