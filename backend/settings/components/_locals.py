# -----------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
# -----------------------------------------------------------------------------
import os

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True
