"""
Development settings
Настройки для локальной разработки
"""

from .base import *

# Debug режим включен
DEBUG = True

# Дополнительные хосты для разработки
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Django Debug Toolbar (установите через requirements/dev.txt)
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

# DRF настройки для разработки - добавляем Browsable API
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',  # Удобный интерфейс для тестирования API
]

# Email backend для разработки - пишет в консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS для разработки - разрешаем все источники
CORS_ALLOW_ALL_ORIGINS = True

# Логирование для разработки
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Отключаем требование HTTPS для разработки
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
