# from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from django.conf import settings

from .api_views import ShortLinkView


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('shortlink', ShortLinkView, basename='short_link')

urlpatterns = router.urls

urlpatterns += [
]
