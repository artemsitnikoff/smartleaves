"""
Команда для генерации preview изображений для worksheet
"""

from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
import random

from apps.worksheets.models import Worksheet


class Command(BaseCommand):
    help = 'Генерирует preview изображения для всех worksheet'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем генерацию preview изображений...\n')

        # Получаем все worksheet без preview
        worksheets = Worksheet.objects.all()
        total = worksheets.count()

        self.stdout.write(f'Найдено worksheet: {total}\n')

        for i, worksheet in enumerate(worksheets, 1):
            try:
                # Генерируем thumbnail и preview
                self.generate_images(worksheet)

                if i % 10 == 0:
                    self.stdout.write(f'  Обработано: {i}/{total}')

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Ошибка для {worksheet.title}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Успешно сгенерировано {total} preview!')
        )

    def generate_images(self, worksheet):
        """Генерирует thumbnail (300x400) и preview (800x1000) для worksheet"""

        # Рандомные цвета для разнообразия
        bg_colors = [
            '#f0f9ff',  # light blue
            '#f0fdf4',  # light green
            '#fef3c7',  # light yellow
            '#fce7f3',  # light pink
            '#f3e8ff',  # light purple
        ]

        accent_colors = [
            '#0ea5e9',  # blue
            '#10b981',  # green
            '#f59e0b',  # orange
            '#ec4899',  # pink
            '#8b5cf6',  # purple
        ]

        bg_color = random.choice(bg_colors)
        accent_color = random.choice(accent_colors)

        # Генерируем thumbnail (300x400)
        thumbnail = self.create_preview_image(
            worksheet,
            (300, 400),
            bg_color,
            accent_color,
            font_size=24
        )

        # Сохраняем thumbnail
        thumb_buffer = BytesIO()
        thumbnail.save(thumb_buffer, format='PNG')
        thumb_buffer.seek(0)

        worksheet.thumbnail.save(
            f'thumb_{worksheet.id}.png',
            File(thumb_buffer),
            save=False
        )

        # Генерируем preview (800x1000)
        preview = self.create_preview_image(
            worksheet,
            (800, 1000),
            bg_color,
            accent_color,
            font_size=48
        )

        # Сохраняем preview
        preview_buffer = BytesIO()
        preview.save(preview_buffer, format='PNG')
        preview_buffer.seek(0)

        worksheet.preview_image.save(
            f'preview_{worksheet.id}.png',
            File(preview_buffer),
            save=False
        )

        worksheet.save()

    def create_preview_image(self, worksheet, size, bg_color, accent_color, font_size):
        """Создает preview изображение"""
        width, height = size

        # Создаем изображение
        img = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(img)

        # Рисуем цветной header
        header_height = height // 4
        draw.rectangle([(0, 0), (width, header_height)], fill=accent_color)

        # Пытаемся загрузить шрифт, если не получается - используем стандартный
        try:
            # Для macOS
            title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', font_size)
            small_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', font_size // 2)
        except:
            title_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Заголовок (белый текст на цветном фоне)
        title = worksheet.title
        if len(title) > 30:
            title = title[:27] + '...'

        # Центрируем текст
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (header_height - text_height) // 2

        draw.text((x, y), title, fill='white', font=title_font)

        # Категория
        category_text = f"Category: {worksheet.category.name}"
        bbox = draw.textbbox((0, 0), category_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = header_height + 40

        draw.text((x, y), category_text, fill=accent_color, font=small_font)

        # Difficulty
        difficulty_map = {
            'easy': 'Easy',
            'medium': 'Medium',
            'hard': 'Hard'
        }
        difficulty_text = f"Level: {difficulty_map.get(worksheet.difficulty, 'Medium')}"
        bbox = draw.textbbox((0, 0), difficulty_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = header_height + 80

        draw.text((x, y), difficulty_text, fill='#666666', font=small_font)

        # Декоративные элементы
        margin = 40

        # Рамка
        draw.rectangle(
            [(margin, header_height + 120), (width - margin, height - margin)],
            outline=accent_color,
            width=3
        )

        # Несколько рандомных кружков для декора
        num_circles = random.randint(3, 6)
        for _ in range(num_circles):
            cx = random.randint(margin + 20, width - margin - 20)
            cy = random.randint(header_height + 140, height - margin - 20)
            radius = random.randint(10, 30)

            # Полупрозрачные круги (эмуляция через lighter color)
            circle_color = self.lighten_color(accent_color, 0.3)
            draw.ellipse(
                [(cx - radius, cy - radius), (cx + radius, cy + radius)],
                fill=circle_color
            )

        return img

    def lighten_color(self, hex_color, factor):
        """Осветляет hex цвет на factor (0.0 - 1.0)"""
        # Убираем #
        hex_color = hex_color.lstrip('#')

        # Конвертируем в RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Осветляем
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)

        return f'#{r:02x}{g:02x}{b:02x}'
