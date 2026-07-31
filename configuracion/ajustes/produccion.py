from .base import *
from decouple import config

DEBUG = False
ALLOWED_HOSTS = ['.onrender.com']
if config('RENDER_EXTERNAL_HOSTNAME', default=''):
    ALLOWED_HOSTS.append(config('RENDER_EXTERNAL_HOSTNAME'))

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='neondb'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {'sslmode': 'require'},
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
