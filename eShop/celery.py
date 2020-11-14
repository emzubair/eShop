import os
from celery import Celery
# Set the default Django setting module for the 'celery' program

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eShop.settings')

app = Celery('eShop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
