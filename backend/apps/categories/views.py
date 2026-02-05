"""
Views для API категорий
"""

from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Category
from .serializers import CategorySerializer, CategoryTreeSerializer


@extend_schema(
    tags=['Категории'],
    summary='Список категорий',
    description='''
    Получить плоский список всех активных категорий.

    Включает родительские категории и их подкатегории.
    Отсортировано по полю order и названию.
    ''',
)
class CategoryListView(generics.ListAPIView):
    """
    Список всех активных категорий
    """
    queryset = Category.objects.filter(is_active=True).order_by('order', 'name')
    serializer_class = CategorySerializer


@extend_schema(
    tags=['Категории'],
    summary='Дерево категорий',
    description='''
    Получить иерархическое дерево категорий (родители с детьми).

    Используется для построения навигационного меню.
    Возвращает только родительские категории первого уровня,
    каждая из которых содержит массив дочерних категорий.

    Максимальная глубина вложенности: 2 уровня.
    ''',
)
class CategoryTreeView(generics.ListAPIView):
    """
    Дерево категорий (родители с детьми)
    """
    queryset = Category.objects.filter(
        is_active=True,
        parent__isnull=True  # Только родительские категории
    ).order_by('order', 'name')
    serializer_class = CategoryTreeSerializer


@extend_schema(
    tags=['Категории'],
    summary='Детали категории',
    description='''
    Получить подробную информацию о конкретной категории по её slug.

    Возвращает информацию о категории, включая количество рабочих листов,
    полный путь для построения URL, и список дочерних категорий если они есть.
    ''',
    parameters=[
        OpenApiParameter(
            name='slug',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='Уникальный slug категории',
            required=True,
        ),
    ],
)
class CategoryDetailView(generics.RetrieveAPIView):
    """
    Детальная информация о категории с дочерними категориями
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryTreeSerializer
    lookup_field = 'slug'
