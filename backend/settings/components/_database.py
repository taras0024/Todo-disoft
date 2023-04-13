import os


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

POSTGRES_DBNAME = os.environ.get('POSTGRES_DBNAME', 'todo')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'pdbuser')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'eUFkAPHVbXMr26kWp4Ws')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DBNAME,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
        'CONN_MAX_AGE': 60 * 2,  # 2 min
    },
}
