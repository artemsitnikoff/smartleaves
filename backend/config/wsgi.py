"""
WSGI config для проекта "Умные листочки"

Используется в production с gunicorn или другими WSGI серверами
"""

import os

from django.core.wsgi import get_wsgi_application

# По умолчанию используем development settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()
