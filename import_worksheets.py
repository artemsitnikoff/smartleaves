#!/usr/bin/env python
"""
Скрипт для импорта рабочих листов из JSON файла в базу данных
ВАЖНО: Перед запуском скрипта убедитесь, что медиа файлы уже скопированы!

Использование: python import_worksheets.py
"""

import json
import os
import sys
import django

# Настройка Django окружения
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from apps.worksheets.models import Worksheet
from apps.categories.models import Category
from apps.tags.models import Tag


def import_worksheets(json_file='worksheets_data.json'):
    """Импортирует рабочие листы из JSON файла"""

    print(f"📂 Чтение данных из {json_file}...")

    with open(json_file, 'r', encoding='utf-8') as f:
        worksheets_data = json.load(f)

    print(f"✅ Найдено {len(worksheets_data)} рабочих листов")
    print(f"📊 Категорий в базе: {Category.objects.count()}")
    print(f"📊 Тегов в базе: {Tag.objects.count()}")

    if Category.objects.count() == 0:
        print("\n❌ ОШИБКА: Сначала импортируйте категории!")
        print("   Запустите: python import_categories.py")
        return 0, 0, 0

    if Tag.objects.count() == 0:
        print("\n⚠️  ПРЕДУПРЕЖДЕНИЕ: Теги не импортированы. Рабочие листы будут без тегов.")
        print("   Рекомендуется сначала запустить: python import_tags.py")

    created_count = 0
    updated_count = 0
    skipped_count = 0
    files_missing_count = 0

    print("\n⏳ Импорт рабочих листов...")
    for ws_data in worksheets_data:
        try:
            # Находим категорию по slug
            category = None
            if ws_data.get('category_slug'):
                try:
                    category = Category.objects.get(slug=ws_data['category_slug'])
                except Category.DoesNotExist:
                    print(f"  ⚠️  Категория '{ws_data['category_slug']}' не найдена для '{ws_data['title']}'")
                    skipped_count += 1
                    continue

            if not category:
                print(f"  ⚠️  У '{ws_data['title']}' нет категории")
                skipped_count += 1
                continue

            # Проверяем наличие PDF файла
            pdf_path = os.path.join('/app/media', ws_data['pdf_file'])
            if not os.path.exists(pdf_path):
                files_missing_count += 1
                # Все равно создаем, но предупреждаем
                # print(f"  ⚠️  PDF файл не найден: {ws_data['pdf_file']}")

            # Создаем или обновляем worksheet
            worksheet, created = Worksheet.objects.update_or_create(
                slug=ws_data['slug'],
                defaults={
                    'title': ws_data['title'],
                    'description': ws_data['description'],
                    'category': category,
                    'grade_level': ws_data['grade_level'],
                    'difficulty': ws_data['difficulty'],
                    'pdf_file': ws_data['pdf_file'],
                    'thumbnail': ws_data['thumbnail'] or '',
                    'preview_image': ws_data['preview_image'] or '',
                    'meta_title': ws_data['meta_title'],
                    'meta_description': ws_data['meta_description'],
                    'is_featured': bool(ws_data['is_featured']),
                    'is_published': bool(ws_data['is_published']),
                }
            )

            # Добавляем теги
            if ws_data.get('tag_slugs'):
                tag_slugs = [s.strip() for s in ws_data['tag_slugs'].split(',') if s.strip()]
                tags = Tag.objects.filter(slug__in=tag_slugs)
                worksheet.tags.set(tags)

            if created:
                created_count += 1
                if created_count % 50 == 0:
                    print(f"  ✅ Создано: {created_count}...")
            else:
                updated_count += 1

        except Exception as e:
            print(f"  ❌ Ошибка при импорте '{ws_data['title']}': {e}")
            skipped_count += 1

    # Итоговая статистика
    print("\n" + "="*60)
    print("📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"  ✅ Создано: {created_count}")
    print(f"  🔄 Обновлено: {updated_count}")
    print(f"  ⏭️  Пропущено: {skipped_count}")
    print(f"  ⚠️  Файлов не найдено: {files_missing_count}")
    print(f"  📦 Всего в базе: {Worksheet.objects.count()}")
    print("="*60)

    if files_missing_count > 0:
        print(f"\n⚠️  Внимание: {files_missing_count} PDF файлов не найдены!")
        print("   Убедитесь, что вы скопировали медиа файлы в /app/media/")

    return created_count, updated_count, skipped_count


if __name__ == '__main__':
    print("🚀 Запуск импорта рабочих листов...")
    print("="*60)

    try:
        import_worksheets()
        print("\n✅ Импорт завершен успешно!")
    except Exception as e:
        print(f"\n❌ Ошибка при импорте: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
