"""
Django Admin для рабочих листов
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Worksheet


@admin.register(Worksheet)
class WorksheetAdmin(admin.ModelAdmin):
    """
    Админка для управления рабочими листами

    Особенности:
    - Автоматическая генерация slug из названия
    - Автоматическая генерация превью из PDF
    - Управление тегами через filter_horizontal
    - Отображение превью в админке
    - Статистика просмотров и скачиваний
    - Массовые действия
    """

    list_display = [
        'thumbnail_preview',
        'title',
        'category',
        'grade_level',
        'difficulty',
        'tags_display',
        'views_count',
        'downloads_count',
        'is_published',
        'is_featured',
        'created_at'
    ]

    list_filter = [
        'is_published',
        'is_featured',
        'category',
        'grade_level',
        'difficulty',
        'created_at'
    ]

    search_fields = ['title', 'description', 'slug']

    prepopulated_fields = {'slug': ('title',)}

    filter_horizontal = ['tags']

    readonly_fields = [
        'views_count',
        'downloads_count',
        'thumbnail_preview_large',
        'preview_image_display',
        'created_at',
        'updated_at',
        'pdf_info'
    ]

    list_editable = ['is_published', 'is_featured']

    date_hierarchy = 'created_at'

    list_per_page = 25

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'category', 'tags'),
            'description': 'Название, описание и категоризация рабочего листа'
        }),
        ('Параметры', {
            'fields': ('grade_level', 'difficulty'),
        }),
        ('Файлы', {
            'fields': (
                'pdf_file',
                'pdf_info',
                'thumbnail_preview_large',
                'preview_image_display'
            ),
            'description': 'PDF файл и автоматически генерируемые превью. '
                          'Превью создаются автоматически при сохранении.'
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Настройки публикации', {
            'fields': ('is_published', 'is_featured', 'published_at'),
        }),
        ('Статистика', {
            'fields': ('views_count', 'downloads_count'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail_preview(self, obj):
        """Маленькое превью для списка"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="60" height="80" '
                'style="object-fit: cover; border: 1px solid #ddd; border-radius: 4px;" />',
                obj.thumbnail.url
            )
        return "Нет превью"
    thumbnail_preview.short_description = 'Превью'

    def thumbnail_preview_large(self, obj):
        """Большое превью миниатюры для детальной страницы"""
        if obj.thumbnail:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p><strong>Миниатюра для каталога (300x400px):</strong></p>'
                '<img src="{}" style="border: 1px solid #ddd; max-width: 300px;" />'
                '</div>',
                obj.thumbnail.url
            )
        return "Превью еще не сгенерировано. Сохраните объект с PDF файлом."
    thumbnail_preview_large.short_description = 'Миниатюра'

    def preview_image_display(self, obj):
        """Большое превью для детальной страницы"""
        if obj.preview_image:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p><strong>Превью для карточки (800x1000px):</strong></p>'
                '<img src="{}" style="border: 1px solid #ddd; max-width: 400px;" />'
                '</div>',
                obj.preview_image.url
            )
        return "Превью еще не сгенерировано. Сохраните объект с PDF файлом."
    preview_image_display.short_description = 'Превью для карточки'

    def pdf_info(self, obj):
        """Информация о PDF файле"""
        if obj.pdf_file:
            try:
                size_mb = obj.pdf_file.size / (1024 * 1024)
                return format_html(
                    '<div style="padding: 10px; background: #f0f0f0; border-radius: 4px;">'
                    '<p><strong>PDF файл:</strong> {}</p>'
                    '<p><strong>Размер:</strong> {:.2f} MB</p>'
                    '<p><strong>URL:</strong> <a href="{}" target="_blank">Открыть PDF</a></p>'
                    '</div>',
                    obj.pdf_file.name.split('/')[-1],
                    size_mb,
                    obj.pdf_file.url
                )
            except:
                return "Информация недоступна"
        return "PDF файл не загружен"
    pdf_info.short_description = 'Информация о PDF'

    def tags_display(self, obj):
        """Отображение тегов в списке"""
        tags = obj.tags.all()[:3]  # Показываем первые 3 тега
        if tags:
            tags_html = ', '.join([f'<span style="background: #e1f5fe; padding: 2px 6px; '
                                   f'border-radius: 3px; font-size: 11px;">{tag.name}</span>'
                                   for tag in tags])
            if obj.tags.count() > 3:
                tags_html += f' <span style="color: #999;">+{obj.tags.count() - 3}</span>'
            return format_html(tags_html)
        return "-"
    tags_display.short_description = 'Теги'

    actions = ['regenerate_previews', 'publish_worksheets', 'unpublish_worksheets', 'make_featured']

    def regenerate_previews(self, request, queryset):
        """
        Массовое действие: пересоздать превью из PDF

        Полезно когда:
        - Изменился алгоритм генерации превью
        - Превью были повреждены
        - Нужно обновить качество изображений
        """
        count = 0
        for worksheet in queryset:
            if worksheet.pdf_file:
                worksheet.generate_previews()
                count += 1

        self.message_user(request, f'Превью пересозданы для {count} рабочих листов')
    regenerate_previews.short_description = '🔄 Пересоздать превью из PDF'

    def publish_worksheets(self, request, queryset):
        """Массовое действие: опубликовать"""
        updated = queryset.update(is_published=True)
        self.message_user(request, f'Опубликовано {updated} рабочих листов')
    publish_worksheets.short_description = '✅ Опубликовать'

    def unpublish_worksheets(self, request, queryset):
        """Массовое действие: снять с публикации"""
        updated = queryset.update(is_published=False)
        self.message_user(request, f'Снято с публикации {updated} рабочих листов')
    unpublish_worksheets.short_description = '❌ Снять с публикации'

    def make_featured(self, request, queryset):
        """Массовое действие: сделать избранными"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'Отмечено как избранное {updated} рабочих листов')
    make_featured.short_description = '⭐ Сделать избранными'

    def save_model(self, request, obj, form, change):
        """
        Переопределяем сохранение для дополнительной логики

        При первом сохранении автоматически устанавливаем published_at
        """
        if not change:  # Если создается новый объект
            if obj.is_published and not obj.published_at:
                from django.utils import timezone
                obj.published_at = timezone.now()

        super().save_model(request, obj, form, change)
