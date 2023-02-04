from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.signals import setup_logging

# set the default Django settings module for the 'celery' program.

BROKER_URL = 'redis://redis:6379'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('shortlink',
             broker=os.environ.get(BROKER_URL),
             backend=os.environ.get(BROKER_URL)
             )

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
