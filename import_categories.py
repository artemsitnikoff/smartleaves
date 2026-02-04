#!/usr/bin/env python
"""
Скрипт для импорта категорий из JSON файла в базу данных
Использование: python import_categories.py
"""

import json
import os
import sys
import django

# Настройка Django окружения
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
django.setup()

from apps.categories.models import Category
from django.utils import timezone


def import_categories(json_file='categories_data.json'):
    """Импортирует категории из JSON файла"""

    print(f"📂 Чтение данных из {json_file}...")

    with open(json_file, 'r', encoding='utf-8') as f:
        categories_data = json.load(f)

    print(f"✅ Найдено {len(categories_data)} категорий")

    # Сначала импортируем родительские категории (без parent_id)
    parent_categories = [cat for cat in categories_data if cat['parent_id'] is None]
    child_categories = [cat for cat in categories_data if cat['parent_id'] is not None]

    print(f"\n📊 Родительских категорий: {len(parent_categories)}")
    print(f"📊 Дочерних категорий: {len(child_categories)}")

    created_count = 0
    updated_count = 0
    skipped_count = 0

    # Словарь для маппинга старых ID на новые объекты
    id_mapping = {}

    # Импортируем родительские категории
    print("\n⏳ Импорт родительских категорий...")
    for cat_data in parent_categories:
        try:
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'] if cat_data['icon'] else '',
                    'order': cat_data['order'],
                    'is_active': bool(cat_data['is_active']),
                }
            )

            id_mapping[cat_data['id']] = category

            if created:
                created_count += 1
                print(f"  ✅ Создана: {category.name}")
            else:
                updated_count += 1
                print(f"  🔄 Обновлена: {category.name}")

        except Exception as e:
            print(f"  ❌ Ошибка при импорте '{cat_data['name']}': {e}")
            skipped_count += 1

    # Импортируем дочерние категории
    print("\n⏳ Импорт дочерних категорий...")
    for cat_data in child_categories:
        try:
            parent_category = id_mapping.get(cat_data['parent_id'])

            if not parent_category:
                print(f"  ⚠️  Родительская категория с ID {cat_data['parent_id']} не найдена для '{cat_data['name']}'")
                skipped_count += 1
                continue

            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'] if cat_data['icon'] else '',
                    'order': cat_data['order'],
                    'is_active': bool(cat_data['is_active']),
                    'parent': parent_category,
                }
            )

            id_mapping[cat_data['id']] = category

            if created:
                created_count += 1
                print(f"  ✅ Создана: {category.name} (родитель: {parent_category.name})")
            else:
                updated_count += 1
                print(f"  🔄 Обновлена: {category.name} (родитель: {parent_category.name})")

        except Exception as e:
            print(f"  ❌ Ошибка при импорте '{cat_data['name']}': {e}")
            skipped_count += 1

    # Итоговая статистика
    print("\n" + "="*60)
    print("📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"  ✅ Создано: {created_count}")
    print(f"  🔄 Обновлено: {updated_count}")
    print(f"  ⏭️  Пропущено: {skipped_count}")
    print(f"  📦 Всего в базе: {Category.objects.count()}")
    print("="*60)

    return created_count, updated_count, skipped_count


if __name__ == '__main__':
    print("🚀 Запуск импорта категорий...")
    print("="*60)

    try:
        import_categories()
        print("\n✅ Импорт завершен успешно!")
    except Exception as e:
        print(f"\n❌ Ошибка при импорте: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
