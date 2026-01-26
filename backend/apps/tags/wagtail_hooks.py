"""
Wagtail ModelAdmin для тегов
Позволяет управлять тегами через интерфейс Wagtail
"""

from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import Tag


class TagAdmin(ModelAdmin):
    """
    Админ-панель для тегов в Wagtail

    Отображает теги с автоматическим подсчетом использования
    """
    model = Tag
    menu_label = 'Теги'
    menu_icon = 'tag'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Колонки в списке
    list_display = ('name', 'slug', 'usage_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')

    # Поля для редактирования
    list_per_page = 50
    ordering = ['-usage_count', 'name']


# Регистрируем в Wagtail
modeladmin_register(TagAdmin)
