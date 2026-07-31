"""
WSGI config for configuracion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


def seleccionar_settings():
    modulo = os.environ.get('DJANGO_SETTINGS_MODULE')
    if modulo:
        return modulo
    if os.environ.get('RENDER') or os.environ.get('VERCEL'):
        return 'configuracion.ajustes.produccion'
    return 'configuracion.ajustes.desarrollo'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', seleccionar_settings())

application = get_wsgi_application()
