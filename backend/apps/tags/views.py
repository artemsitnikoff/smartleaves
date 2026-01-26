"""
Views для API тегов
"""

from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Tag
from .serializers import TagSerializer, TagDetailSerializer


@extend_schema(
    tags=['Теги'],
    summary='Список тегов',
    description='''
    Получить список всех тегов с автоматическим подсчетом использования.

    Теги отсортированы по популярности (usage_count) в порядке убывания.
    Каждый тег содержит количество рабочих листов, в которых он используется.
    ''',
)
class TagListView(generics.ListAPIView):
    """
    Список всех тегов
    """
    queryset = Tag.objects.all().order_by('-usage_count', 'name')
    serializer_class = TagSerializer


@extend_schema(
    tags=['Теги'],
    summary='Детали тега',
    description='''
    Получить подробную информацию о конкретном теге по его slug.

    Включает количество использований и описание тега.
    ''',
    parameters=[
        OpenApiParameter(
            name='slug',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='Уникальный slug тега',
            required=True,
        ),
    ],
)
class TagDetailView(generics.RetrieveAPIView):
    """
    Детальная информация о теге
    """
    queryset = Tag.objects.all()
    serializer_class = TagDetailSerializer
    lookup_field = 'slug'


@extend_schema(
    tags=['Теги'],
    summary='Популярные теги',
    description='''
    Получить топ-20 самых популярных тегов.

    Используется для:
    - Облака тегов на главной странице
    - Sidebar с популярными тегами
    - Быстрой навигации по сайту

    Отсортировано по убыванию usage_count.
    ''',
)
class PopularTagsView(generics.ListAPIView):
    """
    Топ-20 популярных тегов
    """
    queryset = Tag.objects.all().order_by('-usage_count', 'name')[:20]
    serializer_class = TagSerializer
