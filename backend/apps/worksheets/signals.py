"""
Сигналы для автоматического обновления данных
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Worksheet


@receiver(m2m_changed, sender=Worksheet.tags.through)
def update_tag_usage_count(sender, instance, action, **kwargs):
    """
    Автоматически обновляем счетчик usage_count у тегов
    при добавлении/удалении тегов у worksheet

    Вызывается когда:
    - Добавляется тег к worksheet
    - Удаляется тег из worksheet
    - Очищаются все теги у worksheet
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Обновляем счетчики для всех тегов этого worksheet
        for tag in instance.tags.all():
            tag.update_usage_count()

        # Если были удалены теги, обновляем и их
        if action == 'post_remove' and 'pk_set' in kwargs:
            from apps.tags.models import Tag
            for tag_id in kwargs['pk_set']:
                try:
                    tag = Tag.objects.get(pk=tag_id)
                    tag.update_usage_count()
                except Tag.DoesNotExist:
                    pass
