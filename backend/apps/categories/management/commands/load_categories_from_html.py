"""
Команда для загрузки категорий из HTML структуры сайта kiddoworksheets.com
"""
from django.core.management.base import BaseCommand
from apps.categories.models import Category


class Command(BaseCommand):
    help = 'Загружает категории из HTML структуры kiddoworksheets.com'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем загрузку категорий...')

        # Удаляем все worksheets, tags и категории
        from apps.worksheets.models import Worksheet
        from apps.tags.models import Tag

        Worksheet.objects.all().delete()
        self.stdout.write(self.style.WARNING('Удалены все worksheets'))

        Tag.objects.all().delete()
        self.stdout.write(self.style.WARNING('Удалены все tags'))

        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING('Удалены все категории'))

        # Структура категорий из HTML
        categories_structure = [
            {
                'name': 'Alphabets',
                'children': [
                    'Practice Writing Letters',
                    'Cursive Handwriting Practice',
                    'Missing Letters',
                ]
            },
            {
                'name': 'Numbers',
                'children': [
                    'Practice Writing Numbers',
                    'Missing Numbers',
                ]
            },
            {
                'name': 'Maths',
                'children': [
                    'Addition',
                    'Subtraction',
                    'Multiplication',
                    'Multiplication Chart',
                    'Division',
                    'Counting',
                ]
            },
            {
                'name': 'Vocabulary',
                'children': [
                    'Word Search',
                    'Crossword Puzzle',
                    'Spelling Word Scramble',
                    'Sight Words',
                    'English worksheets',
                    'Digraph Spelling Worksheets',
                    'Picture / Shadow Matching',
                    'Find the same',
                    'Find the difference',
                ]
            },
            {'name': 'Shapes', 'children': []},
            {'name': 'Coloring', 'children': []},
            {'name': 'Dot to Dot', 'children': []},
            {'name': 'Drawing', 'children': []},
            {'name': 'GK', 'children': []},
            {'name': 'Body Parts', 'children': []},
            {'name': 'Cartoon Stickers', 'children': []},
            {'name': 'Patterns', 'children': []},
            {'name': 'Flash Cards', 'children': []},
            {'name': 'Telling Time', 'children': []},
            {'name': 'Tracing Lines', 'children': []},
            {'name': 'Sliding Puzzle', 'children': []},
            {'name': 'Origami', 'children': []},
            {'name': 'Mazes', 'children': []},
        ]

        created_count = 0

        # Создаем категории
        for cat_data in categories_structure:
            # Создаем родительскую категорию
            parent = Category.objects.create(
                name=cat_data['name'],
                description=f'{cat_data["name"]} worksheets for kids',
            )
            created_count += 1
            self.stdout.write(f'  Создана категория: {parent.name} (slug: {parent.slug})')

            # Создаем дочерние категории
            for child_name in cat_data['children']:
                child = Category.objects.create(
                    name=child_name,
                    parent=parent,
                    description=f'{child_name} worksheets',
                )
                created_count += 1
                self.stdout.write(f'    → Создана подкатегория: {child.name} (slug: {child.slug})')

        self.stdout.write(
            self.style.SUCCESS(f'\nУспешно создано {created_count} категорий!')
        )
