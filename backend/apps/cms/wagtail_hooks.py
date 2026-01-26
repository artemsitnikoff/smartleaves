"""
Wagtail hooks для кастомизации админки
"""

from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register('construct_main_menu')
def hide_default_menu_items(request, menu_items):
    """
    Кастомизация главного меню Wagtail админки

    Можно скрыть/переименовать пункты меню по необходимости
    """
    # Пример: можно скрыть лишние пункты меню
    # menu_items[:] = [item for item in menu_items if item.name not in ['documents', 'images']]
    pass


@hooks.register('construct_settings_menu')
def hide_settings_menu_items(request, menu_items):
    """
    Кастомизация меню настроек Wagtail
    """
    # Можно скрыть лишние настройки для обычных редакторов
    pass
