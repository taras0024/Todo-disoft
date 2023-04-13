# -----------------------------------------------------------------------------
# Celery common settings
# -----------------------------------------------------------------------------
from celery.schedules import crontab
from kombu import Queue

from backend.settings.components._locals import TIME_ZONE
from backend.settings.components._redis import *

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default'),
)

CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 * 4  # 4 days
CELERY_DISABLE_RATE_LIMITS = True
CELERY_TRACK_STARTED = True

CELERY_IMPORTS = (
    'service.tasks.email_tasks',
)

CELERY_TIMEZONE = TIME_ZONE

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = [CELERY_TASK_SERIALIZER, ]
CELERY_RESULT_SERIALIZER = CELERY_TASK_SERIALIZER

CELERY_RESULT_BACKEND = CRUTCH_CELERY_REDIS_CONNECTION_STRING % REDIS_DBS['CELERY_RESULTS']
CELERY_BACKEND_URL = CELERY_RESULT_BACKEND[:]

CELERYBEAT_SCHEDULE = {}
