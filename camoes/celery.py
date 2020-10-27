from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery
import logging
from celery.schedules import crontab
from celery.task import periodic_task

logger = logging.getLogger('myLog')

logging.debug("Abriue")

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'camoes.settings')

app = Celery('camoes')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(timezone='Europe/Oslo',)
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.enable_utc = False 


@app.task(bind=True)
def debug_task(self):
    return "oi"
    print(f'Request: {self.request!r}')