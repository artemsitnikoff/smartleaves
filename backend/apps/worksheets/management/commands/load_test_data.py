"""
Management команда для загрузки тестовых данных
Создает категории, теги и рабочие листы для тестирования
"""

import os
import random
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

from apps.categories.models import Category
from apps.tags.models import Tag
from apps.worksheets.models import Worksheet


class Command(BaseCommand):
    help = 'Загружает тестовые данные: категории, теги и рабочие листы'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед загрузкой',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка существующих данных...')
            Worksheet.objects.all().delete()
            Tag.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Данные очищены'))

        self.stdout.write('Создание тестовых данных...\n')

        # Создаем категории
        categories = self.create_categories()
        self.stdout.write(self.style.SUCCESS(f'✓ Создано категорий: {len(categories)}'))

        # Создаем теги
        tags = self.create_tags()
        self.stdout.write(self.style.SUCCESS(f'✓ Создано тегов: {len(tags)}'))

        # Создаем рабочие листы
        worksheets_count = self.create_worksheets(categories, tags)
        self.stdout.write(self.style.SUCCESS(f'✓ Создано рабочих листов: {worksheets_count}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Тестовые данные успешно загружены!'))
        self.stdout.write('\nТеперь можно посмотреть:')
        self.stdout.write('  - Админка: http://127.0.0.1:8000/admin/')
        self.stdout.write('  - API категории: http://127.0.0.1:8000/api/categories/')
        self.stdout.write('  - API теги: http://127.0.0.1:8000/api/tags/')
        self.stdout.write('  - API рабочие листы: http://127.0.0.1:8000/api/worksheets/')

    def create_categories(self):
        """Создает иерархию категорий"""
        categories_data = [
            {
                'name': 'Математика',
                'description': 'Обучение счету, сложению, вычитанию и математическим понятиям',
                'children': [
                    {'name': 'Счет до 10', 'description': 'Изучение чисел от 1 до 10'},
                    {'name': 'Счет до 20', 'description': 'Изучение чисел от 11 до 20'},
                    {'name': 'Сложение и вычитание', 'description': 'Простые примеры на сложение и вычитание'},
                ]
            },
            {
                'name': 'Алфавит',
                'description': 'Изучение букв русского алфавита и чтение',
                'children': [
                    {'name': 'Русский алфавит', 'description': 'Изучение букв русского алфавита'},
                    {'name': 'Прописные буквы', 'description': 'Обучение письму прописных букв'},
                    {'name': 'Чтение', 'description': 'Слоги и первые слова'},
                ]
            },
            {
                'name': 'Раскраски',
                'description': 'Развивающие раскраски для детей',
                'children': [
                    {'name': 'Животные', 'description': 'Раскраски с животными'},
                    {'name': 'Транспорт', 'description': 'Машины, самолеты, корабли'},
                    {'name': 'Природа', 'description': 'Цветы, деревья, пейзажи'},
                ]
            },
            {
                'name': 'Логика и внимание',
                'description': 'Развитие логического мышления и внимательности',
                'children': [
                    {'name': 'Головоломки', 'description': 'Логические задачи и головоломки'},
                    {'name': 'Лабиринты', 'description': 'Найди выход из лабиринта'},
                    {'name': 'Найди отличия', 'description': 'Задания на внимательность'},
                ]
            },
        ]

        created_categories = []

        for cat_data in categories_data:
            # Создаем родительскую категорию
            parent = Category.objects.create(
                name=cat_data['name'],
                description=cat_data['description'],
            )
            created_categories.append(parent)
            self.stdout.write(f'  → {parent.name}')

            # Создаем дочерние категории
            for child_data in cat_data.get('children', []):
                child = Category.objects.create(
                    name=child_data['name'],
                    description=child_data['description'],
                    parent=parent,
                )
                created_categories.append(child)
                self.stdout.write(f'    → {child.name}')

        return created_categories

    def create_tags(self):
        """Создает теги"""
        tags_data = [
            {'name': '3-4 года', 'description': 'Для детей 3-4 лет'},
            {'name': '5-6 лет', 'description': 'Для детей 5-6 лет'},
            {'name': '7-8 лет', 'description': 'Для детей 7-8 лет'},
            {'name': '1 класс', 'description': 'Для учеников 1 класса'},
            {'name': '2 класс', 'description': 'Для учеников 2 класса'},
            {'name': 'Легкий уровень', 'description': 'Простые задания'},
            {'name': 'Средний уровень', 'description': 'Задания средней сложности'},
            {'name': 'Сложный уровень', 'description': 'Сложные задания'},
            {'name': 'Цветное', 'description': 'Цветные материалы'},
            {'name': 'Черно-белое', 'description': 'Черно-белые материалы для печати'},
        ]

        created_tags = []
        for tag_data in tags_data:
            tag = Tag.objects.create(
                name=tag_data['name'],
                description=tag_data['description'],
            )
            created_tags.append(tag)

        return created_tags

    def create_worksheets(self, categories, tags):
        """Создает рабочие листы с PDF файлами"""
        # Получаем дочерние категории (не родительские)
        leaf_categories = [cat for cat in categories if cat.children.count() == 0]

        worksheets_data = [
            # Математика - Счет до 10
            {'title': 'Считаем яблочки', 'category': 'Счет до 10', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Научись считать яблочки от 1 до 10', 'tags': ['3-4 года', 'Легкий уровень', 'Цветное']},
            {'title': 'Цифры от 1 до 10', 'category': 'Счет до 10', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Изучаем написание цифр от 1 до 10', 'tags': ['5-6 лет', 'Легкий уровень', 'Черно-белое']},
            {'title': 'Соедини цифру с количеством', 'category': 'Счет до 10', 'grade': 'preschool', 'difficulty': 'medium',
             'description': 'Соедини цифру с нужным количеством предметов', 'tags': ['5-6 лет', 'Средний уровень']},

            # Математика - Счет до 20
            {'title': 'Считаем до 20', 'category': 'Счет до 20', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Учимся считать от 11 до 20', 'tags': ['1 класс', 'Средний уровень']},
            {'title': 'Числа-соседи до 20', 'category': 'Счет до 20', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Найди соседей чисел до 20', 'tags': ['1 класс', 'Средний уровень']},

            # Математика - Сложение и вычитание
            {'title': 'Сложение в пределах 10', 'category': 'Сложение и вычитание', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Простые примеры на сложение', 'tags': ['1 класс', '7-8 лет', 'Средний уровень']},
            {'title': 'Вычитание в пределах 10', 'category': 'Сложение и вычитание', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Простые примеры на вычитание', 'tags': ['1 класс', '7-8 лет', 'Средний уровень']},
            {'title': 'Решаем примеры до 20', 'category': 'Сложение и вычитание', 'grade': 'grade2', 'difficulty': 'hard',
             'description': 'Сложение и вычитание в пределах 20', 'tags': ['2 класс', 'Сложный уровень']},

            # Алфавит - Русский алфавит
            {'title': 'Буква А', 'category': 'Русский алфавит', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Изучаем букву А, учимся писать', 'tags': ['5-6 лет', 'Легкий уровень']},
            {'title': 'Буква Б', 'category': 'Русский алфавит', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Изучаем букву Б, учимся писать', 'tags': ['5-6 лет', 'Легкий уровень']},
            {'title': 'Весь алфавит', 'category': 'Русский алфавит', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Плакат с русским алфавитом', 'tags': ['1 класс', 'Цветное']},

            # Алфавит - Прописные буквы
            {'title': 'Прописные буквы А-Д', 'category': 'Прописные буквы', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Учимся писать прописные буквы', 'tags': ['1 класс', 'Средний уровень']},
            {'title': 'Прописи: соединения букв', 'category': 'Прописные буквы', 'grade': 'grade1', 'difficulty': 'hard',
             'description': 'Учимся соединять буквы', 'tags': ['1 класс', '2 класс', 'Сложный уровень']},

            # Алфавит - Чтение
            {'title': 'Читаем слоги', 'category': 'Чтение', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Учимся читать простые слоги', 'tags': ['1 класс', 'Средний уровень']},
            {'title': 'Первые слова', 'category': 'Чтение', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Читаем простые слова: мама, папа, дом', 'tags': ['1 класс', 'Средний уровень']},

            # Раскраски - Животные
            {'title': 'Раскраска: кошка', 'category': 'Животные', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Раскрась милую кошку', 'tags': ['3-4 года', 'Легкий уровень', 'Черно-белое']},
            {'title': 'Раскраска: собака', 'category': 'Животные', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Раскрась веселую собаку', 'tags': ['3-4 года', 'Легкий уровень', 'Черно-белое']},
            {'title': 'Раскраска: лесные звери', 'category': 'Животные', 'grade': 'preschool', 'difficulty': 'medium',
             'description': 'Раскрась лису, зайца и медведя', 'tags': ['5-6 лет', 'Средний уровень', 'Черно-белое']},

            # Раскраски - Транспорт
            {'title': 'Раскраска: машинка', 'category': 'Транспорт', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Раскрась яркую машинку', 'tags': ['3-4 года', 'Легкий уровень', 'Черно-белое']},
            {'title': 'Раскраска: самолет', 'category': 'Транспорт', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Раскрась самолет в небе', 'tags': ['3-4 года', 'Легкий уровень', 'Черно-белое']},

            # Раскраски - Природа
            {'title': 'Раскраска: цветы', 'category': 'Природа', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Раскрась красивые цветы', 'tags': ['5-6 лет', 'Легкий уровень', 'Черно-белое']},
            {'title': 'Раскраска: дерево', 'category': 'Природа', 'grade': 'preschool', 'difficulty': 'medium',
             'description': 'Раскрась дерево в разные времена года', 'tags': ['5-6 лет', 'Средний уровень', 'Черно-белое']},

            # Логика - Головоломки
            {'title': 'Судоку для детей', 'category': 'Головоломки', 'grade': 'grade2', 'difficulty': 'hard',
             'description': 'Простое судоку с картинками', 'tags': ['2 класс', '7-8 лет', 'Сложный уровень']},
            {'title': 'Логические цепочки', 'category': 'Головоломки', 'grade': 'grade1', 'difficulty': 'medium',
             'description': 'Продолжи логическую последовательность', 'tags': ['1 класс', 'Средний уровень']},

            # Логика - Лабиринты
            {'title': 'Простой лабиринт', 'category': 'Лабиринты', 'grade': 'preschool', 'difficulty': 'easy',
             'description': 'Помоги зайчику найти морковку', 'tags': ['5-6 лет', 'Легкий уровень']},
            {'title': 'Сложный лабиринт', 'category': 'Лабиринты', 'grade': 'grade1', 'difficulty': 'hard',
             'description': 'Найди путь через запутанный лабиринт', 'tags': ['1 класс', '7-8 лет', 'Сложный уровень']},

            # Логика - Найди отличия
            {'title': 'Найди 5 отличий', 'category': 'Найди отличия', 'grade': 'preschool', 'difficulty': 'medium',
             'description': 'Найди 5 отличий между картинками', 'tags': ['5-6 лет', 'Средний уровень']},
            {'title': 'Найди 10 отличий', 'category': 'Найди отличия', 'grade': 'grade1', 'difficulty': 'hard',
             'description': 'Найди 10 отличий - задание для внимательных!', 'tags': ['1 класс', '7-8 лет', 'Сложный уровень']},
        ]

        count = 0
        for ws_data in worksheets_data:
            # Находим категорию
            category = None
            for cat in leaf_categories:
                if cat.name == ws_data['category']:
                    category = cat
                    break

            if not category:
                continue

            # Создаем PDF файл
            pdf_file = self.generate_pdf(ws_data['title'], ws_data['description'])

            # Создаем рабочий лист
            worksheet = Worksheet.objects.create(
                title=ws_data['title'],
                description=ws_data['description'],
                category=category,
                grade_level=ws_data['grade'],
                difficulty=ws_data['difficulty'],
                pdf_file=File(pdf_file, name=f"{ws_data['title']}.pdf"),
                is_published=True,
            )

            # Добавляем теги
            for tag_name in ws_data.get('tags', []):
                tag = Tag.objects.filter(name=tag_name).first()
                if tag:
                    worksheet.tags.add(tag)

            count += 1
            self.stdout.write(f'  → {worksheet.title} ({category.name})')

        return count

    def generate_pdf(self, title, description):
        """Генерирует простой PDF файл с заголовком и описанием"""
        buffer = BytesIO()

        # Создаем PDF
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Заголовок
        p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(width / 2, height - 3*cm, title)

        # Описание
        p.setFont("Helvetica", 14)

        # Разбиваем описание на строки (простой word wrap)
        words = description.split()
        lines = []
        current_line = []
        max_width = width - 4*cm

        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            text_width = p.stringWidth(line_text, "Helvetica", 14)

            if text_width > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Рисуем описание
        y_position = height - 5*cm
        for line in lines:
            p.drawCentredString(width / 2, y_position, line)
            y_position -= 0.7*cm

        # Добавляем рамку
        p.rect(2*cm, 2*cm, width - 4*cm, height - 4*cm)

        # Водяной знак внизу
        p.setFont("Helvetica", 10)
        p.drawCentredString(width / 2, 1.5*cm, "Умные листочки - SmartLeaves.ru")

        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer
