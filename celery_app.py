import os
import time

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.broker_url = settings.CELERY_BROKER_URL
# app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(5)
    print('1--- Hello from debug task!!!')

