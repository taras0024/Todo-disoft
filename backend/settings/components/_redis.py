# -----------------------------------------------------------------------------
# Redis
# -----------------------------------------------------------------------------
import os

REDIS_DBS = {
    'CELERY': 1,
    'CELERY_RESULTS': 2,
}

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or None
REDIS_USE_SSL = os.environ.get('REDIS_USE_SSL', '').upper() in ('TRUE', '1', 'Y', 'YES', 'T')

REDIS_PROTOCOL = 'rediss' if REDIS_USE_SSL else 'redis'
REDIS_AUTH = f'default:{REDIS_PASSWORD}@' if REDIS_PASSWORD else ''

REDIS_CONNECTION = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'password': REDIS_PASSWORD,
}

REDIS_CONNECTION_QUERY = '?ssl_cert_reqs=none' if REDIS_USE_SSL else ''
REDIS_CONNECTION_STRING = '{protocol}://{auth}{host}:{port}/%s{query}'.format(
    protocol=REDIS_PROTOCOL,
    auth=REDIS_AUTH,
    **REDIS_CONNECTION,
    query=REDIS_CONNECTION_QUERY,
)

CRUTCH_CELERY_REDIS_CONNECTION_STRING = REDIS_CONNECTION_STRING.replace('none', 'CERT_NONE')
