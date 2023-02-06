from django.urls import path, include


app_name = 'linkshortener'

urlpatterns = [
    path("v1/", include("linkshortener.api_router")),
]
