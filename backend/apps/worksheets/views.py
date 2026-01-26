"""
Views для API рабочих листов
"""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import Worksheet
from .serializers import WorksheetListSerializer, WorksheetDetailSerializer
from .pagination import WorksheetPagination


@extend_schema(
    tags=['Рабочие листы'],
    summary='Список рабочих листов',
    description='''
    Получить список всех опубликованных рабочих листов с пагинацией.

    Поддерживает фильтрацию по категории, уровню обучения, сложности,
    поиск по названию и описанию, а также сортировку по различным полям.
    ''',
    parameters=[
        OpenApiParameter(
            name='page',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Номер страницы для пагинации',
            required=False,
        ),
        OpenApiParameter(
            name='page_size',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Количество элементов на странице (по умолчанию 20, максимум 100)',
            required=False,
        ),
        OpenApiParameter(
            name='category',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='ID категории для фильтрации',
            required=False,
        ),
        OpenApiParameter(
            name='grade_level',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Уровень обучения (preschool, kindergarten, grade1, grade2, grade3, grade4, grade5)',
            required=False,
        ),
        OpenApiParameter(
            name='difficulty',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Уровень сложности (easy, medium, hard)',
            required=False,
        ),
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Поиск по названию и описанию',
            required=False,
        ),
        OpenApiParameter(
            name='ordering',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Поле для сортировки (created_at, -created_at, views_count, downloads_count, title, -title)',
            required=False,
        ),
    ],
    examples=[
        OpenApiExample(
            'Все листы',
            value='/api/worksheets/',
            request_only=True,
        ),
        OpenApiExample(
            'Фильтр по категории',
            value='/api/worksheets/?category=5',
            request_only=True,
        ),
        OpenApiExample(
            'Поиск',
            value='/api/worksheets/?search=математика',
            request_only=True,
        ),
    ],
)
class WorksheetListView(generics.ListAPIView):
    """
    Список всех рабочих листов для каталога с пагинацией
    """
    queryset = Worksheet.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
    serializer_class = WorksheetListSerializer
    pagination_class = WorksheetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'category__slug', 'grade_level', 'difficulty', 'tags__slug']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'views_count', 'downloads_count', 'title']
    ordering = ['-created_at']


@extend_schema(
    tags=['Рабочие листы'],
    summary='Детали рабочего листа',
    description='''
    Получить подробную информацию о конкретном рабочем листе по его slug.

    При каждом запросе автоматически увеличивается счетчик просмотров.
    Возвращает полную информацию включая большое превью для карточки.
    ''',
    parameters=[
        OpenApiParameter(
            name='slug',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='Уникальный slug рабочего листа',
            required=True,
        ),
    ],
)
class WorksheetDetailView(generics.RetrieveAPIView):
    """
    Детальная информация о рабочем листе (карточка)
    """
    queryset = Worksheet.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
    serializer_class = WorksheetDetailSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        """Переопределяем для увеличения счетчика просмотров"""
        instance = self.get_object()

        # Увеличиваем счетчик просмотров
        instance.increment_views()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(
    tags=['Рабочие листы'],
    summary='Скачать PDF файл',
    description='''
    Скачать PDF файл рабочего листа по его ID.

    При каждом скачивании автоматически увеличивается счетчик downloads_count.
    Возвращает PDF файл с правильным именем для скачивания.
    ''',
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID рабочего листа',
            required=True,
        ),
    ],
    responses={
        200: {
            'type': 'string',
            'format': 'binary',
            'description': 'PDF файл рабочего листа',
        },
        404: {
            'description': 'Рабочий лист или PDF файл не найден',
        },
    },
)
class WorksheetDownloadView(APIView):
    """
    Скачивание PDF файла рабочего листа
    """

    def get(self, request, pk):
        """Скачать PDF по ID worksheet"""
        # Получаем worksheet по ID
        worksheet = get_object_or_404(
            Worksheet.objects.filter(is_published=True),
            pk=pk
        )

        # Проверяем наличие PDF файла
        if not worksheet.pdf_file:
            raise Http404("PDF файл не найден")

        # Увеличиваем счетчик скачиваний
        worksheet.increment_downloads()

        # Возвращаем PDF файл для скачивания
        response = FileResponse(
            worksheet.pdf_file.open('rb'),
            content_type='application/pdf'
        )

        # Устанавливаем заголовок для скачивания файла
        filename = f"{worksheet.slug}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response


class WorksheetSearchView(generics.ListAPIView):
    """
    Поиск рабочих листов с пагинацией

    GET /api/worksheets/search/?q=<запрос>

    Параметры:
    - q: поисковый запрос
    - page: номер страницы

    Примеры:
    - GET /api/worksheets/search/?q=математика
    - GET /api/worksheets/search/?q=сложение&page=2
    """
    serializer_class = WorksheetListSerializer
    pagination_class = WorksheetPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')

        if not query:
            return Worksheet.objects.none()

        return Worksheet.objects.filter(
            is_published=True,
            title__icontains=query
        ).select_related('category').prefetch_related('tags')


class FeaturedWorksheetsView(generics.ListAPIView):
    """
    Избранные рабочие листы для главной страницы

    GET /api/worksheets/featured/

    Возвращает до 12 избранных worksheets без пагинации
    """
    queryset = Worksheet.objects.filter(
        is_published=True,
        is_featured=True
    ).select_related('category').prefetch_related('tags')[:12]
    serializer_class = WorksheetListSerializer


class WorksheetsByCategoryView(generics.ListAPIView):
    """
    Список worksheets по категории с пагинацией

    GET /api/categories/<category_slug>/worksheets/

    Параметры:
    - page: номер страницы
    - page_size: количество элементов

    Если категория родительская - возвращает worksheets из всех дочерних категорий
    Если категория дочерняя - только её worksheets

    Примеры:
    - GET /api/categories/matematika/worksheets/
    - GET /api/categories/matematika/worksheets/?page=2
    - GET /api/categories/slozhenie/worksheets/
    """
    serializer_class = WorksheetListSerializer
    pagination_class = WorksheetPagination

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')

        from apps.categories.models import Category

        # Получаем категорию
        category = get_object_or_404(Category, slug=category_slug, is_active=True)

        # Если это родительская категория - берем worksheets из нее и всех детей
        if category.is_parent:
            # Получаем все дочерние категории
            child_ids = category.children.filter(is_active=True).values_list('id', flat=True)
            category_ids = [category.id] + list(child_ids)

            return Worksheet.objects.filter(
                is_published=True,
                category_id__in=category_ids
            ).select_related('category').prefetch_related('tags')
        else:
            # Если это дочерняя категория - только ее worksheets
            return Worksheet.objects.filter(
                is_published=True,
                category=category
            ).select_related('category').prefetch_related('tags')


class WorksheetsByTagView(generics.ListAPIView):
    """
    Список worksheets по тегу с пагинацией

    GET /api/tags/<tag_slug>/worksheets/

    Параметры:
    - page: номер страницы
    - page_size: количество элементов

    Примеры:
    - GET /api/tags/matematika/worksheets/
    - GET /api/tags/matematika/worksheets/?page=2
    """
    serializer_class = WorksheetListSerializer
    pagination_class = WorksheetPagination

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')

        from apps.tags.models import Tag

        tag = get_object_or_404(Tag, slug=tag_slug)

        return Worksheet.objects.filter(
            is_published=True,
            tags=tag
        ).select_related('category').prefetch_related('tags')


@extend_schema(
    tags=['Рабочие листы'],
    summary='Похожие рабочие листы',
    description='''
    Получить похожие рабочие листы из той же категории.

    Возвращает до 4 рандомных worksheet из той же категории, исключая текущий.
    Полезно для блока "Вам может понравиться" на странице worksheet.
    ''',
    parameters=[
        OpenApiParameter(
            name='slug',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='Slug рабочего листа',
            required=True,
        ),
    ],
)
class WorksheetSimilarView(generics.ListAPIView):
    """
    Получение похожих рабочих листов из той же категории
    """
    serializer_class = WorksheetListSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')

        # Получаем текущий worksheet
        worksheet = get_object_or_404(
            Worksheet.objects.filter(is_published=True),
            slug=slug
        )

        # Возвращаем 4 рандомных worksheet из той же категории (кроме текущего)
        return Worksheet.objects.filter(
            is_published=True,
            category=worksheet.category
        ).exclude(
            id=worksheet.id
        ).select_related('category').prefetch_related('tags').order_by('?')[:4]
