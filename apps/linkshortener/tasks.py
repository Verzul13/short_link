import logging

from django.core.cache import cache
from django.db.models import F

from config.celery import app
from .models import LinkVisit


logger = logging.getLogger("celery")


@app.task
def write_redis_and_create_visit(short_link_id: str, subpart: str, long_url: str) -> None:
    cache.set(f'subpart_{subpart}', long_url, 172800)
    LinkVisit.objects.create(short_link_id=short_link_id)


@app.task
def update_visit_count(subpart: str) -> None:
    LinkVisit.objects.filter(short_link__subpart=subpart).update(visit=F('visit')+1)
