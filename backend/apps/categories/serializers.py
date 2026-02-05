"""
Serializers для API категорий
"""

from rest_framework import serializers
from .models import Category


class CategoryParentSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор родительской категории"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор категории

    Используется:
    - В списке категорий для меню
    - Внутри serializers рабочих листов
    """

    parent = CategoryParentSerializer(read_only=True)
    level = serializers.ReadOnlyField()
    is_parent = serializers.ReadOnlyField()
    full_path = serializers.SerializerMethodField()
    worksheets_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description',
            'parent', 'level', 'is_parent',
            'full_path', 'icon', 'order',
            'worksheets_count'
        ]
        read_only_fields = ['id', 'slug']

    def get_full_path(self, obj):
        """Полный путь категории для URL"""
        return obj.get_full_path()

    def get_worksheets_count(self, obj):
        """Количество worksheets в категории"""
        return obj.get_worksheets_count()


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для дерева категорий (родитель + дети)

    Используется:
    - Для построения меню навигации
    - На главной странице для отображения всех категорий
    """

    parent = CategoryParentSerializer(read_only=True)
    children = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()
    worksheets_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description',
            'parent', 'full_path', 'icon', 'order',
            'worksheets_count', 'children'
        ]

    def get_children(self, obj):
        """Получить дочерние категории если это родитель"""
        if obj.is_parent:
            children = obj.children.filter(is_active=True).order_by('order', 'name')
            return CategorySerializer(children, many=True, context=self.context).data
        return []

    def get_full_path(self, obj):
        """Полный путь категории"""
        return obj.get_full_path()

    def get_worksheets_count(self, obj):
        """Количество worksheets"""
        return obj.get_worksheets_count()
