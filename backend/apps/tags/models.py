"""
Модель тегов для рабочих листов
"""

from django.db import models
from slugify import slugify


class Tag(models.Model):
    """
    Теги для категоризации рабочих листов

    Примеры: математика, сложение, примеры, раскраски, животные
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название тега',
        help_text='Например: математика, сложение, раскраски'
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL slug',
        help_text='Автоматически генерируется из названия'
    )

    description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Описание',
        help_text='Краткое описание тега для SEO'
    )

    # Счетчик использований (денормализация для производительности)
    usage_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество использований',
        help_text='Автоматически обновляется при добавлении/удалении тега'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-usage_count', 'name']
        indexes = [
            models.Index(fields=['-usage_count']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Автоматическая генерация slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def update_usage_count(self):
        """
        Обновить счетчик использований
        Вызывается автоматически через сигналы
        """
        self.usage_count = self.worksheets.filter(is_published=True).count()
        self.save(update_fields=['usage_count'])
