# _*_ encoding:utf-8 _*_
__author__ = 'sunzhaohui'
__date__ = '2019-09-01 11:37'

import os
import django
from celery import Celery,platforms
from django.conf import settings


platforms.C_FORCE_ROOT = True
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reboot.settings')

django.setup()
app = Celery('reboot')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

