"""
Serializers для API тегов
"""

from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор тега

    Используется:
    - В списке тегов
    - Внутри serializers рабочих листов
    - В облаке тегов
    """

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'usage_count']
        read_only_fields = ['id', 'slug', 'usage_count']


class TagDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор тега

    Используется:
    - На странице тега (показывает все worksheets с этим тегом)

    Примечание: worksheets будут добавлены через view с пагинацией
    """

    worksheets_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'description', 'usage_count', 'worksheets_count', 'created_at']
        read_only_fields = ['id', 'slug', 'usage_count', 'created_at']

    def get_worksheets_count(self, obj):
        """Количество опубликованных worksheets с этим тегом"""
        return obj.worksheets.filter(is_published=True).count()
