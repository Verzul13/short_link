import logging

from django.core.cache import cache

from config.celery import app
from .models import LinkVisit


logger = logging.getLogger("celery")


@app.task
def write_redis_and_create_visit(short_link_id: str, subpart: str, long_url: str) -> None:
    cache.set(f'subpart_{subpart}', long_url, 172800)
    LinkVisit.objects.create(short_link_id=short_link_id)
