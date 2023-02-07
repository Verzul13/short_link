from datetime import datetime, timedelta

from django.core.cache import cache
from django.db.models import F

from config.celery import app
from .models import LinkVisit, ShortLink


@app.task
def write_redis_and_create_visit(short_link_id: str, subpart: str, long_url: str) -> None:
    '''
    Записывает subpart в кэш и создает запись в LinkVisit
    '''
    cache.set(f'subpart_{subpart}', long_url, 172800)
    LinkVisit.objects.create(short_link_id=short_link_id)


@app.task
def update_visit_count(subpart: str) -> None:
    '''
    Увеличивает счетчик визитов у модели LinkVisit
    '''
    LinkVisit.objects.filter(short_link__subpart=subpart).update(visits_count=F('visits_count')+1)


@app.task
def delete_old_short_links() -> None:
    '''
    Проставляет ShortLink, которым более двух дней, is_deleted = True
    '''
    # Не удаляем полностью, т.к. статистические данные должны храниться еще какое-то время
    ShortLink.objects.filter(created_dt__lte=datetime.now() - timedelta(days=2)).update(is_deleted=True)
