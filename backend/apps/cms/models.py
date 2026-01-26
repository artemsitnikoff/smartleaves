"""
Wagtail CMS модели страниц и глобальных настроек
"""

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


class HomePage(Page):
    """
    Главная страница сайта

    Управляется через Wagtail CMS
    Может содержать:
    - Hero секцию с заголовком и изображением
    - Описание сайта
    - Настройки для отображения избранных worksheets
    """

    # Hero секция
    hero_title = models.CharField(
        max_length=200,
        verbose_name='Заголовок Hero',
        default='Умные листочки',
        help_text='Основной заголовок на главной странице'
    )

    hero_subtitle = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Подзаголовок Hero',
        help_text='Дополнительный текст под заголовком'
    )

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Hero изображение',
        help_text='Фоновое изображение для Hero секции'
    )

    # Описание
    intro_text = RichTextField(
        blank=True,
        verbose_name='Вводный текст',
        help_text='Текст-описание сайта под Hero секцией'
    )

    # Настройки для панелей Wagtail admin
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_image'),
        FieldPanel('intro_text'),
    ]

    # API поля (для Wagtail API)
    api_fields = [
        APIField('hero_title'),
        APIField('hero_subtitle'),
        APIField('hero_image'),
        APIField('intro_text'),
    ]

    # Ограничение: только одна главная страница
    max_count = 1

    # Родительские страницы: может быть только в корне
    parent_page_types = ['wagtailcore.Page']

    # Дочерние страницы: все типы статических страниц
    subpage_types = ['cms.StaticPage', 'cms.ContactPage', 'cms.AboutPage', 'cms.TermsPage']

    class Meta:
        verbose_name = 'Главная страница'


class StaticPage(Page):
    """
    Статическая страница

    Используется для:
    - О нас
    - Контакты
    - Политика конфиденциальности
    - Пользовательское соглашение
    - FAQ
    - и других информационных страниц
    """

    body = RichTextField(
        verbose_name='Содержимое',
        help_text='Основное содержимое страницы (поддерживает форматирование)'
    )

    # Дополнительные SEO поля
    show_in_footer = models.BooleanField(
        default=False,
        verbose_name='Показывать в футере',
        help_text='Добавить ссылку на эту страницу в футер сайта'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('show_in_footer'),
    ]

    api_fields = [
        APIField('body'),
        APIField('show_in_footer'),
    ]

    # Родительские страницы
    parent_page_types = ['cms.HomePage']

    # Дочерние страницы: не может иметь детей
    subpage_types = []

    class Meta:
        verbose_name = 'Статическая страница'
        verbose_name_plural = 'Статические страницы'


class ContactPage(Page):
    """
    Страница контактов

    Специализированная страница для контактной информации
    Можно расширить дополнительными полями (адрес, карта и т.д.)
    """

    body = RichTextField(
        verbose_name='Основной текст',
        help_text='Текст страницы контактов'
    )

    # Контактная информация (опционально, дублирует SiteSettings)
    email = models.EmailField(
        blank=True,
        verbose_name='Email',
        help_text='Контактный email (опционально, если отличается от основного)'
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Телефон',
        help_text='Контактный телефон (опционально, если отличается от основного)'
    )

    address = models.TextField(
        blank=True,
        verbose_name='Адрес',
        help_text='Физический адрес офиса/организации'
    )

    show_in_footer = models.BooleanField(
        default=True,
        verbose_name='Показывать в футере'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone'),
            FieldPanel('address'),
        ], heading='Контактная информация'),
        FieldPanel('show_in_footer'),
    ]

    api_fields = [
        APIField('body'),
        APIField('email'),
        APIField('phone'),
        APIField('address'),
        APIField('show_in_footer'),
    ]

    parent_page_types = ['cms.HomePage']
    subpage_types = []
    max_count = 1  # Только одна страница контактов

    class Meta:
        verbose_name = 'Страница контактов'


class AboutPage(Page):
    """
    Страница "О проекте"

    Специализированная страница для описания проекта
    """

    intro = models.TextField(
        verbose_name='Краткое описание',
        help_text='Краткое описание проекта (1-2 предложения)',
        blank=True
    )

    body = RichTextField(
        verbose_name='Полное описание',
        help_text='Подробное описание проекта, его целей и задач'
    )

    mission = RichTextField(
        blank=True,
        verbose_name='Наша миссия',
        help_text='Описание миссии проекта'
    )

    show_in_footer = models.BooleanField(
        default=True,
        verbose_name='Показывать в футере'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('mission'),
        FieldPanel('show_in_footer'),
    ]

    api_fields = [
        APIField('intro'),
        APIField('body'),
        APIField('mission'),
        APIField('show_in_footer'),
    ]

    parent_page_types = ['cms.HomePage']
    subpage_types = []
    max_count = 1  # Только одна страница "О проекте"

    class Meta:
        verbose_name = 'Страница "О проекте"'


class TermsPage(Page):
    """
    Страница "Правила использования контента"

    Юридическая информация об использовании материалов сайта
    """

    body = RichTextField(
        verbose_name='Правила использования',
        help_text='Полный текст правил использования контента сайта'
    )

    last_updated = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата последнего обновления',
        help_text='Когда правила были обновлены последний раз'
    )

    show_in_footer = models.BooleanField(
        default=True,
        verbose_name='Показывать в футере'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('last_updated'),
        FieldPanel('show_in_footer'),
    ]

    api_fields = [
        APIField('body'),
        APIField('last_updated'),
        APIField('show_in_footer'),
    ]

    parent_page_types = ['cms.HomePage']
    subpage_types = []
    max_count = 1  # Только одна страница правил

    class Meta:
        verbose_name = 'Правила использования контента'


@register_setting
class SiteSettings(BaseSiteSetting):
    """
    Глобальные настройки сайта

    Доступны во всех шаблонах через {{ settings.cms.SiteSettings }}
    Через API: GET /api/settings/

    Используется для:
    - Контактной информации (email, телефон)
    - Текста для главной страницы
    - Текста в хедере
    - Других глобальных параметров
    """

    # === КОНТАКТНАЯ ИНФОРМАЦИЯ ===

    contact_email = models.EmailField(
        blank=True,
        verbose_name='Email для связи',
        help_text='Основной email для связи с администрацией'
    )

    contact_phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Телефон для связи',
        help_text='Основной телефон для связи'
    )

    # === ТЕКСТЫ ДЛЯ САЙТА ===

    header_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Текст в хедере',
        help_text='Короткий текст/слоган отображаемый в шапке сайта'
    )

    home_page_intro = RichTextField(
        blank=True,
        verbose_name='Вводный текст на главной',
        help_text='Текст, отображаемый на главной странице под Hero секцией'
    )

    footer_text = models.TextField(
        blank=True,
        verbose_name='Текст в футере',
        help_text='Текст, отображаемый в футере сайта (копирайт, описание и т.д.)'
    )

    # === СОЦИАЛЬНЫЕ СЕТИ ===

    telegram_url = models.URLField(
        blank=True,
        verbose_name='Telegram',
        help_text='Ссылка на канал/группу в Telegram'
    )

    # === НАСТРОЙКИ ОТОБРАЖЕНИЯ ===

    worksheets_per_page = models.PositiveIntegerField(
        default=20,
        verbose_name='Рабочих листов на странице',
        help_text='Количество рабочих листов на одной странице каталога'
    )

    show_stats = models.BooleanField(
        default=True,
        verbose_name='Показывать статистику',
        help_text='Отображать счетчики просмотров и скачиваний'
    )

    # Панели для Wagtail Admin
    panels = [
        MultiFieldPanel([
            FieldPanel('contact_email'),
            FieldPanel('contact_phone'),
        ], heading='📞 Контактная информация'),

        MultiFieldPanel([
            FieldPanel('header_text'),
            FieldPanel('home_page_intro'),
            FieldPanel('footer_text'),
        ], heading='📝 Тексты для сайта'),

        MultiFieldPanel([
            FieldPanel('telegram_url'),
        ], heading='📱 Социальные сети'),

        MultiFieldPanel([
            FieldPanel('worksheets_per_page'),
            FieldPanel('show_stats'),
        ], heading='⚙️ Настройки отображения'),
    ]

    class Meta:
        verbose_name = 'Настройки сайта'
