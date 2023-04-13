# -----------------------------------------------------------------------------
# Static
# -----------------------------------------------------------------------------
import os

from backend.settings.components._paths import PROJECT_DIR
from backend.settings.tools import utils

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'media', 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media', 'uploads')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

utils.create_directories(
    os.path.join(PROJECT_DIR, 'static')
)
