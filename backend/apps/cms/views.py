"""
Views для CMS API
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from wagtail.models import Site
from drf_spectacular.utils import extend_schema

from .models import SiteSettings
from .serializers import SiteSettingsSerializer


@extend_schema(
    tags=['Настройки'],
    summary='Глобальные настройки сайта',
    description='''
    Получить глобальные настройки сайта из Wagtail CMS.

    Возвращает:
    - Контактную информацию (email, телефон)
    - Тексты для сайта (хедер, главная страница, футер)
    - Ссылки на социальные сети (Telegram)
    - Настройки отображения (количество элементов на странице, показывать ли статистику)

    Эти настройки можно изменить через Wagtail Admin в разделе Settings → Настройки сайта.
    ''',
    responses={
        200: SiteSettingsSerializer,
    },
)
class SiteSettingsView(APIView):
    """
    Глобальные настройки сайта
    """

    def get(self, request):
        """Получить настройки для текущего сайта"""
        # Получаем текущий Site (Wagtail поддерживает multi-site)
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            site = Site.objects.first()

        # Получаем настройки для этого сайта
        settings = SiteSettings.for_site(site)

        # Сериализуем и возвращаем
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)
