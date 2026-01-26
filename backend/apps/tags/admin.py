"""
Django Admin для тегов
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Админка для управления тегами

    Особенности:
    - Автоматическая генерация slug
    - Автоматический подсчет использований
    - Сортировка по популярности
    """

    list_display = [
        'name',
        'slug',
        'usage_count_display',
        'created_at'
    ]

    search_fields = ['name', 'slug', 'description']

    prepopulated_fields = {'slug': ('name',)}

    readonly_fields = ['usage_count', 'created_at']

    list_per_page = 50

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Статистика', {
            'fields': ('usage_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def usage_count_display(self, obj):
        """Отображение количества использований с иконкой"""
        if obj.usage_count > 10:
            color = 'green'
        elif obj.usage_count > 5:
            color = 'orange'
        else:
            color = 'gray'

        return format_html(
            '<span style="color: {}; font-weight: bold;">📊 {}</span>',
            color,
            obj.usage_count
        )
    usage_count_display.short_description = 'Использований'
    usage_count_display.admin_order_field = 'usage_count'

    actions = ['update_usage_counts']

    def update_usage_counts(self, request, queryset):
        """Действие для обновления счетчиков использований"""
        count = 0
        for tag in queryset:
            tag.update_usage_count()
            count += 1

        self.message_user(request, f'Счетчики обновлены для {count} тегов')
    update_usage_counts.short_description = 'Обновить счетчики использований'
