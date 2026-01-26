"""
Модель рабочих листов (worksheets)
"""

from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile
from slugify import slugify
from PIL import Image
import io
import os

# Для генерации превью из PDF
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False


class GradeLevel(models.TextChoices):
    """Уровни обучения (возраст/класс)"""
    PRESCHOOL = 'preschool', 'Дошкольники (3-4 года)'
    KINDERGARTEN = 'kindergarten', 'Подготовительная группа (5-6 лет)'
    GRADE_1 = 'grade1', '1 класс'
    GRADE_2 = 'grade2', '2 класс'
    GRADE_3 = 'grade3', '3 класс'
    GRADE_4 = 'grade4', '4 класс'
    GRADE_5 = 'grade5', '5 класс'


class Difficulty(models.TextChoices):
    """Уровень сложности"""
    EASY = 'easy', 'Легкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'


class Worksheet(models.Model):
    """
    Рабочий лист - основная сущность приложения

    Содержит:
    - PDF файл для печати
    - Автоматически генерируемые превью (миниатюра и большое)
    - Связь с категорией и тегами
    - Статистику просмотров и скачиваний
    """

    # === ОСНОВНАЯ ИНФОРМАЦИЯ ===

    title = models.CharField(
        max_length=300,
        verbose_name='Название',
        help_text='Например: Сложение чисел в пределах 10'
    )

    slug = models.SlugField(
        max_length=300,
        unique=True,
        verbose_name='URL slug',
        help_text='Автоматически генерируется из названия'
    )

    description = models.TextField(
        verbose_name='Описание',
        help_text='Подробное описание рабочего листа'
    )

    # === КАТЕГОРИЗАЦИЯ ===

    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        related_name='worksheets',
        verbose_name='Категория',
        help_text='Выберите категорию (предпочтительно 2-го уровня)'
    )

    tags = models.ManyToManyField(
        'tags.Tag',
        related_name='worksheets',
        blank=True,
        verbose_name='Теги',
        help_text='Выберите теги для этого рабочего листа'
    )

    # === ПАРАМЕТРЫ ===

    grade_level = models.CharField(
        max_length=20,
        choices=GradeLevel.choices,
        verbose_name='Уровень обучения',
        help_text='Для какого возраста/класса предназначен'
    )

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
        verbose_name='Сложность'
    )

    # === ФАЙЛЫ ===

    pdf_file = models.FileField(
        upload_to='worksheets/pdf/%Y/%m/',
        validators=[FileExtensionValidator(['pdf'])],
        verbose_name='PDF файл',
        help_text='Рабочий лист в формате PDF для печати'
    )

    # Маленькое превью для каталога (автоматически генерируется)
    thumbnail = models.ImageField(
        upload_to='worksheets/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Миниатюра для каталога',
        help_text='Автоматически генерируется из PDF (300x400px)'
    )

    # Большое превью для карточки (автоматически генерируется)
    preview_image = models.ImageField(
        upload_to='worksheets/previews/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Превью для карточки',
        help_text='Автоматически генерируется из PDF (800x1000px)'
    )

    # === SEO ===

    meta_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='SEO заголовок',
        help_text='Если не указан, используется title'
    )

    meta_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='SEO описание',
        help_text='Краткое описание для поисковых систем'
    )

    # === СТАТИСТИКА ===

    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров',
        help_text='Увеличивается при открытии карточки'
    )

    downloads_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество скачиваний',
        help_text='Увеличивается при скачивании PDF'
    )

    # === ФЛАГИ ===

    is_featured = models.BooleanField(
        default=False,
        verbose_name='Избранный',
        help_text='Отображать на главной странице'
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Неопубликованные листы скрыты от пользователей'
    )

    # === ДАТЫ ===

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рабочий лист'
        verbose_name_plural = 'Рабочие листы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['grade_level']),
            models.Index(fields=['is_featured', '-created_at']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Переопределяем save для:
        1. Автоматической генерации slug
        2. Генерации превью из PDF
        """
        # Генерируем slug из названия если не указан
        if not self.slug:
            self.slug = slugify(self.title)

        # Сохраняем объект первый раз чтобы получить файл
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Если PDF загружен и превью еще нет - генерируем
        if self.pdf_file and (not self.thumbnail or not self.preview_image or is_new):
            self.generate_previews()

    def generate_previews(self):
        """
        Генерирует два превью изображения из первой страницы PDF:
        1. Миниатюру для каталога (300x400px)
        2. Большое превью для карточки (800x1000px)

        ВАЖНО: Требует установки poppler-utils:
        - macOS: brew install poppler
        - Ubuntu: sudo apt-get install poppler-utils
        - Windows: скачать бинарники poppler
        """
        if not PDF2IMAGE_AVAILABLE:
            print("⚠️  Warning: pdf2image не установлен. Превью не будут генерироваться.")
            print("   Установите: pip install pdf2image")
            print("   И poppler: brew install poppler (macOS)")
            return

        try:
            # Получаем путь к PDF файлу
            pdf_path = self.pdf_file.path

            # Конвертируем первую страницу PDF в изображение
            # dpi=200 для хорошего качества
            images = convert_from_path(
                pdf_path,
                first_page=1,
                last_page=1,
                dpi=200
            )

            if not images:
                print(f"❌ Не удалось конвертировать PDF '{self.title}'")
                return

            first_page = images[0]

            # === 1. Генерируем миниатюру для каталога (300x400) ===
            thumbnail = first_page.copy()
            thumbnail.thumbnail((300, 400), Image.Resampling.LANCZOS)

            # Сохраняем в BytesIO
            thumb_io = io.BytesIO()
            thumbnail.save(thumb_io, format='PNG', optimize=True)
            thumb_io.seek(0)

            # Генерируем имя файла
            thumb_filename = f"{self.slug}_thumb.png"

            # Сохраняем в поле модели
            self.thumbnail.save(
                thumb_filename,
                ContentFile(thumb_io.read()),
                save=False
            )

            # === 2. Генерируем большое превью для карточки (800x1000) ===
            preview = first_page.copy()
            preview.thumbnail((800, 1000), Image.Resampling.LANCZOS)

            preview_io = io.BytesIO()
            preview.save(preview_io, format='PNG', optimize=True)
            preview_io.seek(0)

            preview_filename = f"{self.slug}_preview.png"

            self.preview_image.save(
                preview_filename,
                ContentFile(preview_io.read()),
                save=False
            )

            # Сохраняем модель с новыми превью
            super().save(update_fields=['thumbnail', 'preview_image'])

            print(f"✅ Превью успешно сгенерированы для '{self.title}'")

        except Exception as e:
            print(f"❌ Ошибка при генерации превью для '{self.title}': {e}")

    def increment_views(self):
        """
        Увеличить счетчик просмотров (при открытии карточки)
        """
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_downloads(self):
        """
        Увеличить счетчик скачиваний (при скачивании PDF)
        """
        self.downloads_count += 1
        self.save(update_fields=['downloads_count'])

    def get_absolute_url(self):
        """
        Получить URL карточки worksheet

        Возвращает:
            str: URL, например '/matematika/slozhenie/primery-do-10/'
        """
        return f"/{self.category.get_full_path()}/{self.slug}/"
