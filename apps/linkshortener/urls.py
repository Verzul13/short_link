from django.urls import path

from linkshortener.api_views import test

app_name = 'linkshortener'

urlpatterns = [
    path("test/", test, name='test')
]
