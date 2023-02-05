from django.shortcuts import redirect
from django.core.cache import cache

from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema

from .swagger_schema import REDIRECT_SUBPART_PARAMETER
from .models import ShortLink
from .utils import ValidationError
from .tasks import update_visit_count


@swagger_auto_schema(**REDIRECT_SUBPART_PARAMETER, method='GET', tags=["app"])
@api_view(['GET'], )
def redirect_subpart(request):
    '''
    Принимает subpart и редиректит на записынный в кэш или ShortLink url
    '''
    subpart = request.GET.get('subpart')
    url = cache.get(f'subpart_{subpart}')
    if not url:
        short_link = ShortLink.objects.filter(subpart=subpart).first()
        if not short_link:
            return ValidationError('Redirect url is missing')
        url = short_link.long_url

    update_visit_count.delay(subpart)

    return redirect(url)
