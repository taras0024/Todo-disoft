# -*- coding: utf-8 -*-
import os
import warnings

from split_settings.tools import include

warnings.filterwarnings('ignore', category=DeprecationWarning)

ENV = os.environ.get('DJANGO_ENV') or 'local'
assert ENV in {'local', 'dev', 'prod'}, 'Use only allowed environments'

COMPONENTS_DIR = os.path.join(os.path.dirname(__file__), 'components')

include(
    os.path.join(COMPONENTS_DIR, '_paths.py'),
    os.path.join(COMPONENTS_DIR, '_base.py'),
    os.path.join(COMPONENTS_DIR, '_apps.py'),
    os.path.join(COMPONENTS_DIR, '_templates.py'),
    os.path.join(COMPONENTS_DIR, '_middleware.py'),
    os.path.join(COMPONENTS_DIR, '_static.py'),
    os.path.join(COMPONENTS_DIR, '_logger.py'),
    os.path.join(COMPONENTS_DIR, '_locals.py'),
    os.path.join(COMPONENTS_DIR, '_database.py'),
    os.path.join(COMPONENTS_DIR, '_redis.py'),
    os.path.join(COMPONENTS_DIR, '_rabbit.py'),
    os.path.join(COMPONENTS_DIR, '_celery.py'),
    os.path.join(COMPONENTS_DIR, '_jazzmin.py'),
    os.path.join(COMPONENTS_DIR, '_rest.py'),
)

include(os.path.join('environments', '{}.py'.format(ENV)))
