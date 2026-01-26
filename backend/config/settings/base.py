"""
Django settings для проекта "Умные листочки"
Базовые настройки (общие для dev и prod)

Для работы требуется:
- Python 3.11+
- PostgreSQL 15+
- poppler-utils (для генерации превью из PDF)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Wagtail CMS
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',  # Для глобальных настроек сайта
    'wagtail_modeladmin',  # Для управления Django моделями через Wagtail
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtail.api.v2',

    'modelcluster',
    'taggit',

    # Django REST Framework
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_spectacular',  # API документация (Swagger/OpenAPI)

    # Наши приложения
    'apps.worksheets',
    'apps.categories',
    'apps.tags',
    'apps.cms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS должен быть перед CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',  # Глобальные настройки Wagtail
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Для удобства первого запуска используем SQLite
# Чтобы использовать PostgreSQL, измените настройки ниже
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Чтобы использовать PostgreSQL, раскомментируйте и измените SQLite выше:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME', 'smartleaves'),
#         'USER': os.getenv('DB_USER', 'postgres'),
#         'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ====================
# WAGTAIL SETTINGS
# ====================

WAGTAIL_SITE_NAME = 'Умные листочки'
WAGTAIL_FRONTEND_LOGIN_URL = '/admin/login/'

# Базовый URL для Wagtail API (если нужен)
WAGTAILADMIN_BASE_URL = os.getenv('WAGTAIL_BASE_URL', 'http://localhost:8000')


# ====================
# DJANGO REST FRAMEWORK
# ====================

REST_FRAMEWORK = {
    # Пагинация по умолчанию (переопределяется в views где нужно)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    # Фильтры
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Рендереры (JSON по умолчанию)
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    # Парсеры
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],

    # Аутентификация (пока без регистрации - только для админа)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],

    # Permissions (публичный доступ для чтения)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    # API документация (Swagger/OpenAPI)
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# ====================
# SWAGGER/OPENAPI SETTINGS
# ====================

SPECTACULAR_SETTINGS = {
    'TITLE': 'Умные листочки API',
    'DESCRIPTION': '''
    API для образовательного портала "Умные листочки"

    Основные возможности:
    - Получение списка рабочих листов с фильтрацией и поиском
    - Категории и подкатегории (2-уровневая иерархия)
    - Теги с автоматическим подсчетом использования
    - Скачивание PDF файлов
    - Глобальные настройки сайта

    Все API endpoints доступны публично (без авторизации).
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    # Контактная информация
    'CONTACT': {
        'name': 'Умные листочки',
        'email': 'info@smartleaves.ru',
    },

    # Лицензия
    'LICENSE': {
        'name': 'Proprietary',
    },

    # Настройки отображения
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': True,

    # Теги для группировки endpoints
    'TAGS': [
        {'name': 'Рабочие листы', 'description': 'Операции с рабочими листами'},
        {'name': 'Категории', 'description': 'Категории рабочих листов'},
        {'name': 'Теги', 'description': 'Теги для рабочих листов'},
        {'name': 'Настройки', 'description': 'Глобальные настройки сайта'},
    ],

    # Примеры значений
    'ENUM_NAME_OVERRIDES': {
        'GradeLevel': 'apps.worksheets.models.GradeLevel',
        'Difficulty': 'apps.worksheets.models.Difficulty',
    },
}


# ====================
# CORS SETTINGS
# ====================
# Для работы Vue.js фронтенда с другого порта/домена

CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173'
).split(',')

CORS_ALLOW_CREDENTIALS = True


# ====================
# FILE UPLOAD SETTINGS
# ====================

# Максимальный размер загружаемых файлов (50 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB

# Допустимые форматы файлов
ALLOWED_UPLOAD_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
