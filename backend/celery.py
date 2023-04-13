# -*- coding: utf-8 -*-
"""
Description of Celery application.
"""
import os

import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.base')

app = celery.Celery('todo-app')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
