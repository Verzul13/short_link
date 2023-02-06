from django.core.validators import RegexValidator

from rest_framework import serializers

from .models import ShortLink


class ShortLinkSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortLink
        exclude = ['created_dt', 'updated_dt', 'is_deleted']

    def get_full_url(self, obj: ShortLink):
        from .api_views import create_full_url
        return create_full_url(self.context['request'], obj.subpart)


class ShortLinkCreateSerializer(serializers.ModelSerializer):

    link = serializers.URLField(help_text="Long URL")
    subpart = serializers.CharField(min_length=6, max_length=6, validators=[
        RegexValidator("^[a-zA-Z0-9]+$", message='Must consist of letters or numbers')],
        help_text="Subpart", required=False)

    class Meta:
        model = ShortLink
        exclude = ['created_dt', 'updated_dt', 'is_deleted']
