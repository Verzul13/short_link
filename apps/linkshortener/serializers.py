from django.core.validators import RegexValidator

from rest_framework import serializers

from .models import ShortLink


class ShortLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortLink
        exclude = ['created_dt', 'updated_dt', 'is_deleted']


class ShortLinkCreateSerializer(serializers.ModelSerializer):

    long_url = serializers.URLField(help_text="Long URL")
    subpart = serializers.CharField(min_length=6, max_length=6, validators=[
        RegexValidator("^[a-zA-Z0-9]+$", message='Must consist of letters or numbers')],
        help_text="Subpart", required=False)

    class Meta:
        model = ShortLink
        exclude = ['created_dt', 'updated_dt', 'is_deleted']
