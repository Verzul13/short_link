"""fintech_trader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

from linkshortener.views import MainPageView, redirect_subpart


schema_view = get_schema_view(
    openapi.Info(
        title="Shortlink API",
        default_version='v1',
        description="REST API for Shortlink service",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=settings.SWAGGER_URL
)

urlpatterns = [
    path('system/admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico')),),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("<str:subpart>", redirect_subpart, name='redirect_subpart'),
    path("api/", include("linkshortener.urls", namespace='linkshortener')),
    path('main_page/', MainPageView.as_view(), name='main_page'),
    path('system/', include('django_prometheus.urls')),
]
