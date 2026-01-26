"""
Модель категорий для рабочих листов
Максимум 2 уровня вложенности: Родитель → Ребенок
"""

from django.db import models
from django.core.exceptions import ValidationError
from slugify import slugify


class Category(models.Model):
    """
    Категория рабочих листов (максимум 2 уровня)

    Примеры:
    - Математика (родитель)
      - Сложение (ребенок)
      - Вычитание (ребенок)

    URL: /matematika/slozhenie/
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Например: Математика, Сложение'
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL slug',
        help_text='Автоматически генерируется из названия. Используется в URL'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория',
        help_text='Оставьте пустым для главной категории'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Краткое описание категории для SEO'
    )

    icon = models.ImageField(
        upload_to='categories/icons/',
        null=True,
        blank=True,
        verbose_name='Иконка',
        help_text='Иконка для отображения в меню'
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки',
        help_text='Чем меньше число, тем выше в списке'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Неактивные категории скрыты на сайте'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['parent', 'is_active']),
            models.Index(fields=['order']),
        ]

    def __str__(self):
        """Строковое представление"""
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name

    def clean(self):
        """
        Валидация модели
        Запрещаем создание категорий 3-го уровня
        """
        if self.parent and self.parent.parent:
            raise ValidationError(
                'Нельзя создать категорию 3-го уровня. '
                'Максимум 2 уровня: Родитель → Ребенок'
            )

    def save(self, *args, **kwargs):
        """Автоматическая генерация slug и валидация"""
        # Генерируем slug из названия если не указан
        if not self.slug:
            self.slug = slugify(self.name)

        # Валидация перед сохранением
        self.clean()

        super().save(*args, **kwargs)

    def get_full_path(self):
        """
        Получить полный путь категории для URL

        Возвращает:
            str: Полный путь, например 'matematika/slozhenie'
        """
        if self.parent:
            return f"{self.parent.slug}/{self.slug}"
        return self.slug

    @property
    def level(self):
        """
        Уровень вложенности категории

        Возвращает:
            int: 1 для родительской, 2 для дочерней
        """
        return 2 if self.parent else 1

    @property
    def is_parent(self):
        """
        Является ли категория родительской

        Возвращает:
            bool: True если это родительская категория
        """
        return self.parent is None

    def get_worksheets_count(self):
        """
        Получить количество рабочих листов в этой категории
        Для родительской категории - сумма из всех дочерних

        Возвращает:
            int: Количество worksheets
        """
        if self.is_parent:
            # Для родителя - считаем из всех детей
            count = self.worksheets.filter(is_published=True).count()
            for child in self.children.filter(is_active=True):
                count += child.worksheets.filter(is_published=True).count()
            return count
        else:
            # Для ребенка - только свои
            return self.worksheets.filter(is_published=True).count()
