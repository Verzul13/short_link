from django.urls import path, include

from .views import redirect_subpart


app_name = 'linkshortener'

urlpatterns = [
    path("v1/", include("linkshortener.api_router")),
    path("", redirect_subpart, name='redirect_subpart')
]
