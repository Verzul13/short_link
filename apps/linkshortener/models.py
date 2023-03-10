import uuid
from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

from .managers import IsDeletedManager


class AbstractBaseModel(models.Model):
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_dt = models.DateTimeField(_('Date of creation'), auto_now_add=True, editable=False)
    updated_dt = models.DateTimeField(_('Date of update'), auto_now=True, editable=True)
    is_deleted = models.BooleanField(_('Deleted'), default=False)

    objects = IsDeletedManager()  # Manager

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.updated_dt = datetime.now()

        return super().save(force_insert, force_update, using, update_fields)


class ShortLink(AbstractBaseModel):
    long_url = models.URLField(_('Long URL'), blank=True, null=True)
    subpart = models.CharField(_("Subpart"), max_length=128, null=True, blank=True)
    session_key = models.CharField(_("Session key"), max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'Short link'
        verbose_name_plural = 'Short links'

    def __str__(self):
        return f'{self.long_url}: {self.subpart}'


class LinkVisit(AbstractBaseModel):
    short_link = models.ForeignKey(ShortLink, on_delete=models.CASCADE)
    visits_count = models.PositiveIntegerField(_('Visits count'), default=0)

    class Meta:
        verbose_name = 'Link visit'
        verbose_name_plural = 'Link visits'

    def __str__(self):
        return f'{self.short_link}: {self.visits_count}'
