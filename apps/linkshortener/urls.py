from django.urls import path, include

from linkshortener.api_views import test

app_name = 'linkshortener'

urlpatterns = [
    path("test/", test, name='test')
]
