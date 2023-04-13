import os

from corsheaders.defaults import default_headers

"""
Base settings shared by all platforms.

Quick-start development settings - unsuitable for production
See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-^e44go#*2aft=1eg3q#-)irpmse7x@t$i%ach8ah92*q)r&3nr')
HOSTNAME = os.environ.get('HOSTNAME', '127.0.0.1')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -----------------------------------------------------------------------------
# Django mptt
# -----------------------------------------------------------------------------
MPTT_ADMIN_LEVEL_INDENT = 32

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+(-\w+)?\.{}\.{}$".format(*HOSTNAME.split('.')[-2:]),
]
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_HEADERS = list(default_headers) + [
    'EXTRA-HEADER',
]

# -----------------------------------------------------------------------------
# Substituting a custom User model
# -----------------------------------------------------------------------------
AUTH_USER_MODEL = 'users.User'

# -----------------------------------------------------------------------------
# ShellPlus
# -----------------------------------------------------------------------------
SHELL_PLUS = 'ipython'

# -----------------------------------------------------------------------------
# SMTP
# -----------------------------------------------------------------------------
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND') or 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST') or 'smtp.gmail.com'
EMAIL_PORT = int(os.environ.get('EMAIL_PORT') or 587)
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').upper() in ('TRUE', '1', 'YES', 'Y', 'T')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
