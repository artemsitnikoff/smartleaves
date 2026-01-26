"""
Django Admin для категорий
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для управления категориями

    Особенности:
    - Автоматическая генерация slug из названия
    - Валидация максимум 2 уровней вложенности
    - Отображение иконок в списке
    - Фильтрация по родительской категории
    """

    list_display = [
        'icon_preview',
        'name',
        'slug',
        'parent',
        'level',
        'worksheets_count',
        'order',
        'is_active'
    ]

    list_filter = ['is_active', 'parent', 'created_at']

    search_fields = ['name', 'slug', 'description']

    prepopulated_fields = {'slug': ('name',)}

    list_editable = ['order', 'is_active']

    readonly_fields = ['level', 'created_at', 'updated_at', 'icon_preview']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Оформление', {
            'fields': ('icon', 'icon_preview', 'order')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
        ('Системная информация', {
            'fields': ('level', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def icon_preview(self, obj):
        """Показать превью иконки в админке"""
        if obj.icon:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.icon.url
            )
        return "Нет иконки"
    icon_preview.short_description = 'Превью иконки'

    def worksheets_count(self, obj):
        """Количество рабочих листов в категории"""
        count = obj.get_worksheets_count()
        return format_html('<strong>{}</strong>', count)
    worksheets_count.short_description = 'Кол-во листов'

    def level(self, obj):
        """Уровень категории"""
        if obj.is_parent:
            return format_html('<span style="color: green;">1 (Родитель)</span>')
        return format_html('<span style="color: blue;">2 (Ребенок)</span>')
    level.short_description = 'Уровень'
