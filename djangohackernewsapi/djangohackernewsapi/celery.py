from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from decouple import config

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangohackernewsapi.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('settings', default='djangohackernewsapi.settings'))

app = Celery('djangohackernewsapi')



# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
# print('Request: {0!r}'.format(self.request))
    print(f'Request: {self.request!r}')