from django.contrib import admin

from .models import ShortLink, LinkVisit


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ('long_url', 'subpart')


@admin.register(LinkVisit)
class LinkVisitAdmin(admin.ModelAdmin):
    list_display = ('short_link', 'visits_count')
