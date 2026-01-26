"""
URL Configuration для проекта "Умные листочки"

Главный роутер для всех URL маршрутов
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Django Admin (стандартная админка Django)
    # URL: /django-admin/
    path('django-admin/', admin.site.urls),

    # Wagtail Admin (CMS админка)
    # URL: /admin/
    path('admin/', include(wagtailadmin_urls)),

    # Wagtail Documents
    path('documents/', include(wagtaildocs_urls)),

    # API endpoints
    path('api/settings/', include('apps.cms.urls')),  # Глобальные настройки сайта
    path('api/worksheets/', include('apps.worksheets.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/tags/', include('apps.tags.urls')),

    # API документация (Swagger/OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Wagtail CMS pages (должен быть последним!)
    # Обслуживает все остальные URL через Wagtail
    path('', include(wagtail_urls)),
]

# Настройка для обслуживания медиа файлов в development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django Debug Toolbar (только в development)
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Кастомизация заголовков админки
admin.site.site_header = 'Умные листочки - Администрирование'
admin.site.site_title = 'Умные листочки Admin'
admin.site.index_title = 'Управление сайтом'
