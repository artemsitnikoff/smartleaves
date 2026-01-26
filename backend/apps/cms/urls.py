"""
URL маршруты для CMS API
"""

from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # Глобальные настройки сайта
    # GET /api/settings/
    path('', views.SiteSettingsView.as_view(), name='settings'),
]
