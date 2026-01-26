"""
Serializers для API рабочих листов
"""

from rest_framework import serializers
from .models import Worksheet
from apps.tags.serializers import TagSerializer
from apps.categories.serializers import CategorySerializer


class WorksheetListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка worksheets (каталог)

    Используется:
    - В каталоге всех worksheets
    - В списках по категориям
    - В списках по тегам
    - В результатах поиска

    Возвращает компактную информацию + миниатюру для каталога
    """

    tags = TagSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    category_path = serializers.CharField(source='category.get_full_path', read_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Worksheet
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'category_name',
            'category_slug',
            'category_path',
            'grade_level',
            'difficulty',
            'thumbnail',           # Маленькое превью для каталога
            'tags',
            'views_count',
            'downloads_count',
            'download_url',
            'created_at'
        ]

    def get_download_url(self, obj):
        """URL для скачивания PDF"""
        return f"/api/worksheets/{obj.id}/download/"


class WorksheetDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор для карточки worksheet

    Используется:
    - На странице отдельного рабочего листа
    - Показывает полную информацию + большое превью

    При обращении к этому сериализатору увеличивается
    счетчик просмотров (реализовано в view)
    """

    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    download_url = serializers.SerializerMethodField()
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Worksheet
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'category',
            'grade_level',
            'difficulty',
            'preview_image',       # Большое превью для карточки
            'thumbnail',           # Маленькое тоже (на случай если нужно)
            'tags',
            'views_count',
            'downloads_count',
            'download_url',
            'absolute_url',
            'meta_title',
            'meta_description',
            'created_at',
            'updated_at'
        ]

    def get_download_url(self, obj):
        """URL для скачивания PDF"""
        return f"/api/worksheets/{obj.id}/download/"
