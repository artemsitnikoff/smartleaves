#!/usr/bin/env python
"""
Скрипт для импорта тегов из JSON файла в базу данных
Использование: python import_tags.py
"""

import json
import os
import sys
import django

# Настройка Django окружения
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from apps.tags.models import Tag


def import_tags(json_file='tags_data.json'):
    """Импортирует теги из JSON файла"""

    print(f"📂 Чтение данных из {json_file}...")

    with open(json_file, 'r', encoding='utf-8') as f:
        tags_data = json.load(f)

    print(f"✅ Найдено {len(tags_data)} тегов")

    created_count = 0
    updated_count = 0
    skipped_count = 0

    print("\n⏳ Импорт тегов...")
    for tag_data in tags_data:
        try:
            tag, created = Tag.objects.update_or_create(
                slug=tag_data['slug'],
                defaults={
                    'name': tag_data['name'],
                    'description': tag_data['description'],
                }
            )

            if created:
                created_count += 1
                print(f"  ✅ Создан: {tag.name}")
            else:
                updated_count += 1
                print(f"  🔄 Обновлен: {tag.name}")

        except Exception as e:
            print(f"  ❌ Ошибка при импорте '{tag_data['name']}': {e}")
            skipped_count += 1

    # Итоговая статистика
    print("\n" + "="*60)
    print("📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"  ✅ Создано: {created_count}")
    print(f"  🔄 Обновлено: {updated_count}")
    print(f"  ⏭️  Пропущено: {skipped_count}")
    print(f"  📦 Всего в базе: {Tag.objects.count()}")
    print("="*60)

    return created_count, updated_count, skipped_count


if __name__ == '__main__':
    print("🚀 Запуск импорта тегов...")
    print("="*60)

    try:
        import_tags()
        print("\n✅ Импорт завершен успешно!")
    except Exception as e:
        print(f"\n❌ Ошибка при импорте: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
