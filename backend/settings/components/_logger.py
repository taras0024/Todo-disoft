# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
import os

from backend.settings.components._paths import LOG_ROOT

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logsna': {
            '()': 'logsna.Formatter',
        }
    },
    'handlers': {
        'backend': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,  # 5 MiB
            'backupCount': 20,
            'filename': os.path.join(LOG_ROOT, 'todo-app.log'),
            'formatter': 'logsna',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['backend'],
            'level': 'INFO',
            'propagate': True,
        },
        'service': {
            'handlers': ['backend'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
