import os

# настройка celery
from celery.schedules import crontab

from config.settings import TIME_ZONE

RABBIT_LOGIN = os.environ.get("RABBITMQ_USER", "")
RABBIT_PASS = os.environ.get("RABBITMQ_PASS", "")
RABBIT_VHOST = os.environ.get("RABBITMQ_VHOST", "")
RABBIT_HOST = os.environ.get("RABBITMQ_HOST", "broker.example.com")

CELERY_BROKER_URL = f'amqp://{RABBIT_LOGIN}:{RABBIT_PASS}@{RABBIT_HOST}:5672{RABBIT_VHOST}'
BROKER_URL = CELERY_BROKER_URL
CELERY_BROKER = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")

CELERY_TIMEZONE = TIME_ZONE
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_WORKER_CONCURRENCY = 1   # this is the one I was actually looking for
CELERY_MAX_TASKS_PER_CHILD = 2


CELERY_BEAT_SCHEDULE = {
    # every day once a day
    'delete_old_short_links': {
        'task': 'linkshortener.tasks.delete_old_short_links',
        'schedule': crontab(minute=0, hour=0),
        'args': ()
    },
}
