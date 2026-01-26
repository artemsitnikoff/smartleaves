"""
Команда для загрузки категорий из JSON файла
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from apps.categories.models import Category


class Command(BaseCommand):
    help = 'Загружает категории из JSON файла'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем загрузку категорий из JSON...')

        # Читаем JSON файл
        json_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'categories.json'

        with open(json_path, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)

        created_count = 0
        parent_order = 0

        # Создаем категории
        for cat_data in categories_data:
            parent_order += 1

            # Создаем родительскую категорию
            parent = Category.objects.create(
                name=cat_data['title'],
                description=f'{cat_data["title"]} worksheets for kids',
                order=parent_order,
            )
            created_count += 1
            self.stdout.write(f'  Создана категория: {parent.name} (slug: {parent.slug}, order: {parent.order})')

            # Создаем дочерние категории
            child_order = 0
            for child_data in cat_data.get('children', []):
                child_order += 1
                child = Category.objects.create(
                    name=child_data['title'],
                    parent=parent,
                    description=f'{child_data["title"]} worksheets',
                    order=child_order,
                )
                created_count += 1
                self.stdout.write(f'    → Создана подкатегория: {child.name} (slug: {child.slug}, order: {child.order})')

        self.stdout.write(
            self.style.SUCCESS(f'\nУспешно создано {created_count} категорий!')
        )
