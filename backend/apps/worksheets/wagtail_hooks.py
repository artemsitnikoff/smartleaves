"""
Wagtail ModelAdmin для рабочих листов
Позволяет управлять рабочими листами через интерфейс Wagtail
"""

from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.utils.html import format_html
from .models import Worksheet


class WorksheetAdmin(ModelAdmin):
    """
    Админ-панель для рабочих листов в Wagtail

    Позволяет:
    - Загружать PDF файлы
    - Автоматически генерировать превью
    - Назначать категории и теги
    - Отслеживать статистику
    """
    model = Worksheet
    menu_label = 'Рабочие листы'
    menu_icon = 'doc-full-inverse'
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Колонки в списке
    list_display = (
        'thumbnail_preview',
        'title',
        'category',
        'grade_level',
        'difficulty',
        'stats',
        'is_published',
        'created_at'
    )
    list_filter = (
        'is_published',
        'grade_level',
        'difficulty',
        'category',
        'created_at'
    )
    search_fields = ('title', 'description')

    # Поля для редактирования
    list_per_page = 20
    ordering = ['-created_at']

    # Группировка полей при редактировании
    form_fields_exclude = ['slug', 'views_count', 'downloads_count']

    # Панели для редактирования
    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('description'),
            FieldPanel('category'),
        ], heading='Основная информация'),

        MultiFieldPanel([
            FieldPanel('pdf_file'),
            FieldPanel('thumbnail'),
            FieldPanel('preview_image'),
        ], heading='Файлы и изображения'),

        MultiFieldPanel([
            FieldPanel('grade_level'),
            FieldPanel('difficulty'),
            FieldPanel('tags'),
        ], heading='Характеристики'),

        MultiFieldPanel([
            FieldPanel('is_published'),
        ], heading='Публикация'),
    ]

    def thumbnail_preview(self, obj):
        """Показывает миниатюру в списке"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 60px; height: 80px; object-fit: cover; border-radius: 4px;" />',
                obj.thumbnail.url
            )
        return format_html(
            '<div style="width: 60px; height: 80px; background: #f0f0f0; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #999;">Нет превью</div>'
        )

    thumbnail_preview.short_description = 'Превью'

    def stats(self, obj):
        """Показывает статистику просмотров и скачиваний"""
        return format_html(
            '<div style="font-size: 11px;">'
            '<div>👁 {}</div>'
            '<div>⬇ {}</div>'
            '</div>',
            obj.views_count,
            obj.downloads_count
        )

    stats.short_description = 'Статистика'


# Регистрируем в Wagtail
modeladmin_register(WorksheetAdmin)
