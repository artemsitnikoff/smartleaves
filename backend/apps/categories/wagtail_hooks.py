"""
Wagtail ModelAdmin для категорий
Позволяет управлять категориями через интерфейс Wagtail
"""

from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import Category


class CategoryAdmin(ModelAdmin):
    """
    Админ-панель для категорий в Wagtail

    Отображает категории в двухуровневой иерархии
    с возможностью фильтрации и поиска
    """
    model = Category
    menu_label = 'Категории'
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Колонки в списке
    list_display = ('name', 'parent', 'get_level', 'get_worksheets_count', 'order', 'is_active')
    list_filter = ('parent', 'is_active')
    search_fields = ('name', 'description')

    # Поля для редактирования
    list_per_page = 50
    ordering = ['parent', 'order', 'name']

    def get_level(self, obj):
        """Уровень вложенности категории"""
        return obj.level

    get_level.short_description = 'Уровень'
    get_level.admin_order_field = 'parent'  # Позволяет сортировать по родителю

    def get_worksheets_count(self, obj):
        """Количество рабочих листов в категории"""
        return obj.get_worksheets_count()

    get_worksheets_count.short_description = 'Кол-во листов'


# Регистрируем в Wagtail
modeladmin_register(CategoryAdmin)
