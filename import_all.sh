#!/bin/bash

# Скрипт для полного импорта всех данных на production
# Использование: ./import_all.sh

set -e

echo "🚀 Запуск полного импорта данных..."
echo "="*60

# Проверяем наличие файлов
if [ ! -f "categories_data.json" ]; then
    echo "❌ Файл categories_data.json не найден!"
    exit 1
fi

if [ ! -f "tags_data.json" ]; then
    echo "❌ Файл tags_data.json не найден!"
    exit 1
fi

if [ ! -f "worksheets_data.json" ]; then
    echo "❌ Файл worksheets_data.json не найден!"
    exit 1
fi

# 1. Импорт категорий
echo ""
echo "📦 Шаг 1/4: Импорт категорий..."
docker cp categories_data.json smartleaves_backend:/app/
docker cp import_categories.py smartleaves_backend:/app/
docker compose -f docker-compose.prod.yml exec backend python /app/import_categories.py

# 2. Импорт тегов
echo ""
echo "📦 Шаг 2/4: Импорт тегов..."
docker cp tags_data.json smartleaves_backend:/app/
docker cp import_tags.py smartleaves_backend:/app/
docker compose -f docker-compose.prod.yml exec backend python /app/import_tags.py

# 3. Медиа файлы
echo ""
echo "📦 Шаг 3/4: Копирование медиа файлов..."
if [ -f "media_files.tar.gz" ]; then
    echo "Распаковка media_files.tar.gz..."
    tar -xzf media_files.tar.gz
    echo "Копирование файлов в контейнер..."
    docker cp media/. smartleaves_backend:/app/media/
    echo "✅ Медиа файлы скопированы"

    # Проверка
    FILES_COUNT=$(docker compose -f docker-compose.prod.yml exec backend ls /app/media/ | wc -l)
    echo "📊 Файлов в /app/media/: $FILES_COUNT"
else
    echo "⚠️  media_files.tar.gz не найден, пропускаем..."
    echo "   Скопируйте архив на сервер: scp media_files.tar.gz deploy@server:/var/www/smartleaves/"
fi

# 4. Импорт worksheets
echo ""
echo "📦 Шаг 4/4: Импорт рабочих листов..."
docker cp worksheets_data.json smartleaves_backend:/app/
docker cp import_worksheets.py smartleaves_backend:/app/
docker compose -f docker-compose.prod.yml exec backend python /app/import_worksheets.py

# Итоговая проверка
echo ""
echo "="*60
echo "✅ ИМПОРТ ЗАВЕРШЕН!"
echo "="*60
echo ""
echo "📊 Проверьте через API:"
echo "  Категории: curl https://smartleaves.dclouds.ru/api/categories/ | jq '. | length'"
echo "  Теги:      curl https://smartleaves.dclouds.ru/api/tags/ | jq '.results | length'"
echo "  Worksheets: curl https://smartleaves.dclouds.ru/api/worksheets/ | jq '.count'"
echo ""
echo "🌐 Или откройте в браузере:"
echo "  https://smartleaves.dclouds.ru"
echo ""
