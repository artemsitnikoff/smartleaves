"""
Management команда для генерации 100 тестовых worksheet
"""

import random
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files import File

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor

from apps.categories.models import Category
from apps.tags.models import Tag
from apps.worksheets.models import Worksheet


class Command(BaseCommand):
    help = 'Генерирует тестовые worksheet с рандомными данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Количество worksheet для генерации (по умолчанию 100)'
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(f'Начинаем генерацию {count} worksheet...\n')

        # Создаем теги если их нет
        tags = self.create_tags()
        self.stdout.write(self.style.SUCCESS(f'✓ Теги готовы: {len(tags)}'))

        # Получаем категории (только листовые - без детей)
        leaf_categories = list(Category.objects.filter(children=None))
        if not leaf_categories:
            self.stdout.write(self.style.ERROR('Ошибка: нет категорий в базе!'))
            return

        self.stdout.write(self.style.SUCCESS(f'✓ Категорий для распределения: {len(leaf_categories)}'))

        # Генерируем worksheet
        self.stdout.write('\nГенерация worksheet:')
        start_index = Worksheet.objects.count() + 1
        for i in range(start_index, start_index + count):
            worksheet = self.create_random_worksheet(i, leaf_categories, tags)
            current = i - start_index + 1
            if current % 50 == 0 or current == count:
                self.stdout.write(f'  Создано: {current}/{count}')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Успешно создано {count} worksheet!'))
        self.stdout.write('\nТеперь можно посмотреть:')
        self.stdout.write('  - API: http://127.0.0.1:8000/api/worksheets/')
        self.stdout.write('  - Swagger: http://127.0.0.1:8000/api/docs/')

    def create_tags(self):
        """Создает теги если их нет"""
        tags_data = [
            # Возраст
            {'name': 'Age 3-4', 'description': 'For kids 3-4 years old'},
            {'name': 'Age 5-6', 'description': 'For kids 5-6 years old'},
            {'name': 'Age 7-8', 'description': 'For kids 7-8 years old'},
            {'name': 'Age 9-10', 'description': 'For kids 9-10 years old'},

            # Классы
            {'name': 'Preschool', 'description': 'For preschool kids'},
            {'name': 'Kindergarten', 'description': 'For kindergarten'},
            {'name': 'Grade 1', 'description': 'For 1st grade students'},
            {'name': 'Grade 2', 'description': 'For 2nd grade students'},
            {'name': 'Grade 3', 'description': 'For 3rd grade students'},

            # Уровни сложности
            {'name': 'Easy', 'description': 'Easy level'},
            {'name': 'Medium', 'description': 'Medium level'},
            {'name': 'Hard', 'description': 'Hard level'},

            # Типы
            {'name': 'Colorful', 'description': 'Color worksheets'},
            {'name': 'Black & White', 'description': 'Printable black and white'},
            {'name': 'Practice', 'description': 'Practice worksheets'},
            {'name': 'Fun', 'description': 'Fun activities'},
            {'name': 'Educational', 'description': 'Educational content'},
            {'name': 'Creative', 'description': 'Creative activities'},

            # Темы
            {'name': 'Animals', 'description': 'Animal themed'},
            {'name': 'Nature', 'description': 'Nature themed'},
            {'name': 'Numbers', 'description': 'Number worksheets'},
            {'name': 'Letters', 'description': 'Letter worksheets'},
            {'name': 'Shapes', 'description': 'Shapes and geometry'},
            {'name': 'Colors', 'description': 'Color learning'},
        ]

        created_tags = []
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'description': tag_data['description']}
            )
            created_tags.append(tag)

        return created_tags

    def create_random_worksheet(self, index, categories, tags):
        """Создает один рандомный worksheet"""

        # Рандомная категория
        category = random.choice(categories)

        # Рандомные параметры
        grade_choices = ['preschool', 'kindergarten', 'grade1', 'grade2', 'grade3']
        difficulty_choices = ['easy', 'medium', 'hard']

        grade = random.choice(grade_choices)
        difficulty = random.choice(difficulty_choices)

        # Генерируем название и описание
        title = self.generate_title(category, index)
        description = self.generate_description(category, difficulty)

        # Создаем PDF
        pdf_file = self.generate_pdf(title, description, category.name, difficulty)

        # Создаем worksheet
        worksheet = Worksheet.objects.create(
            title=title,
            description=description,
            category=category,
            grade_level=grade,
            difficulty=difficulty,
            pdf_file=File(pdf_file, name=f"worksheet_{index}.pdf"),
            is_published=True,
        )

        # Добавляем 2-5 рандомных тегов
        num_tags = random.randint(2, 5)
        selected_tags = random.sample(tags, num_tags)
        worksheet.tags.set(selected_tags)

        return worksheet

    def generate_title(self, category, index):
        """Генерирует рандомное название"""
        templates = [
            f"{category.name} Worksheet #{index}",
            f"Practice {category.name} #{index}",
            f"Fun {category.name} Activity #{index}",
            f"Learn {category.name} #{index}",
            f"{category.name} Exercise #{index}",
            f"{category.name} Practice Sheet #{index}",
            f"Master {category.name} #{index}",
            f"{category.name} Skills #{index}",
        ]
        return random.choice(templates)

    def generate_description(self, category, difficulty):
        """Генерирует рандомное описание"""
        intros = [
            "This worksheet helps children",
            "Kids will practice",
            "Students will learn",
            "Great activity for",
            "Perfect for learning",
            "Fun way to practice",
            "Educational worksheet for",
            "Engaging activity to master",
        ]

        middles = [
            f"{category.name.lower()} skills",
            f"essential {category.name.lower()} concepts",
            f"important {category.name.lower()} topics",
            f"fundamental {category.name.lower()} knowledge",
        ]

        endings = [
            f"Difficulty level: {difficulty}.",
            f"Suitable for {difficulty} learners.",
            "Great for classroom or home use.",
            "Print and practice anytime!",
            "Colorful and engaging design.",
            "Perfect for independent learning.",
        ]

        intro = random.choice(intros)
        middle = random.choice(middles)
        ending = random.choice(endings)

        return f"{intro} {middle}. {ending}"

    def generate_pdf(self, title, description, category_name, difficulty):
        """Генерирует PDF файл с рандомным дизайном"""
        buffer = BytesIO()

        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Рандомный цвет для заголовка
        colors = [
            HexColor('#0ea5e9'),  # Blue
            HexColor('#10b981'),  # Green
            HexColor('#f59e0b'),  # Orange
            HexColor('#8b5cf6'),  # Purple
            HexColor('#ef4444'),  # Red
        ]
        header_color = random.choice(colors)

        # Заголовок с цветным фоном
        p.setFillColor(header_color)
        p.rect(0, height - 4*cm, width, 4*cm, fill=1)

        p.setFillColor(HexColor('#ffffff'))
        p.setFont("Helvetica-Bold", 22)
        p.drawCentredString(width / 2, height - 2.5*cm, title)

        # Категория
        p.setFont("Helvetica", 12)
        p.drawCentredString(width / 2, height - 3.2*cm, f"Category: {category_name} | Difficulty: {difficulty.upper()}")

        # Основной контент
        p.setFillColor(HexColor('#000000'))
        p.setFont("Helvetica", 14)

        # Описание
        y_pos = height - 6*cm
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

        for line in lines:
            p.drawCentredString(width / 2, y_pos, line)
            y_pos -= 0.8*cm

        # Рандомные декоративные элементы
        p.setStrokeColor(header_color)
        p.setLineWidth(2)

        # Несколько рандомных фигур
        num_shapes = random.randint(3, 8)
        for _ in range(num_shapes):
            shape_type = random.choice(['circle', 'rect', 'line'])
            x = random.uniform(3*cm, width - 3*cm)
            y = random.uniform(3*cm, height - 8*cm)

            if shape_type == 'circle':
                p.circle(x, y, 0.5*cm)
            elif shape_type == 'rect':
                p.rect(x, y, 1*cm, 1*cm)
            else:
                p.line(x, y, x + 2*cm, y + 1*cm)

        # Рамка
        p.setStrokeColor(HexColor('#000000'))
        p.setLineWidth(1)
        p.rect(1.5*cm, 1.5*cm, width - 3*cm, height - 3*cm)

        # Футер
        p.setFont("Helvetica", 10)
        p.setFillColor(HexColor('#666666'))
        p.drawCentredString(width / 2, 1*cm, "SmartLeaves - Educational Worksheets for Kids")

        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer
