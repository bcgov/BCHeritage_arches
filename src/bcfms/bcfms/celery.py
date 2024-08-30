from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

import platform

if platform.system().lower() == "windows":
    os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bcfms.settings')
app = Celery(settings.CELERY_WORKER_NAME)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
