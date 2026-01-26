"""
Serializers для CMS API
"""

from rest_framework import serializers
from .models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для глобальных настроек сайта

    Используется для передачи настроек на фронтенд через API:
    - Контактная информация
    - Тексты для сайта
    - Социальные сети
    - Настройки отображения
    """

    class Meta:
        model = SiteSettings
        fields = [
            # Контакты
            'contact_email',
            'contact_phone',

            # Тексты
            'header_text',
            'home_page_intro',
            'footer_text',

            # Социальные сети
            'telegram_url',

            # Настройки
            'worksheets_per_page',
            'show_stats',
        ]
