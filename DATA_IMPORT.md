# Инструкция по импорту данных на production

Этот файл содержит инструкции по переносу данных из локальной разработки на production сервер.

## Что нужно импортировать

1. **Категории** (40 шт.) - `categories_data.json`
2. **Теги** (24 шт.) - `tags_data.json`
3. **Рабочие листы** (900 шт.) - `worksheets_data.json`
4. **Медиа файлы** (2728 файлов, ~61 МБ) - `media_files.tar.gz`

## Шаг 1: Подготовка файлов

### На локальной машине:

```bash
# Убедитесь, что все файлы созданы
ls -lh categories_data.json tags_data.json worksheets_data.json media_files.tar.gz

# Скопируйте файлы на сервер
scp categories_data.json tags_data.json worksheets_data.json \
    import_categories.py import_tags.py import_worksheets.py \
    media_files.tar.gz \
    deploy@37.9.5.160:/var/www/smartleaves/
```

## Шаг 2: Импорт на сервере

### На сервере выполните команды по порядку:

```bash
cd /var/www/smartleaves

# 1. Импортируйте категории (ОБЯЗАТЕЛЬНО ПЕРВЫМ!)
echo "📦 Импорт категорий..."
docker cp categories_data.json smartleaves_backend:/app/
docker cp import_categories.py smartleaves_backend:/app/
docker compose -f docker-compose.prod.yml exec backend python /app/import_categories.py

# 2. Импортируйте теги
echo "📦 Импорт тегов..."
docker cp tags_data.json smartleaves_backend:/app/
docker cp import_tags.py smartleaves_backend:/app/
docker compose -f docker-compose.prod.yml exec backend python /app/import_tags.py

# 3. Распакуйте медиа файлы в volume
echo "📦 Распаковка медиа файлов..."
tar -xzf media_files.tar.gz
docker cp media/. smartleaves_backend:/app/media/

# Проверьте что файлы скопировались
docker compose -f docker-compose.prod.yml exec backend ls -lh /app/media/ | head -20

# 4. Импортируйте рабочие листы (ПОСЛЕДНИМ!)
echo "📦 Импорт рабочих листов..."
docker cp worksheets_data.json smartleaves_backend:/app/
docker cp import_worksheets.py smartleaves_backend:/app/
docker compose -f docker-compose.prod.yml exec backend python /app/import_worksheets.py
```

## Шаг 3: Проверка

### Проверьте через API:

```bash
# Категории (должно быть 40)
curl https://smartleaves.dclouds.ru/api/categories/ | jq '. | length'

# Теги (должно быть 24)
curl https://smartleaves.dclouds.ru/api/tags/ | jq '.results | length'

# Рабочие листы (должно быть 900)
curl https://smartleaves.dclouds.ru/api/worksheets/ | jq '.count'
```

### Или через админку:

- Категории: `https://smartleaves.dclouds.ru/admin/snippets/categories/category/`
- Теги: `https://smartleaves.dclouds.ru/admin/tags/tag/`
- Рабочие листы: `https://smartleaves.dclouds.ru/admin/worksheets/worksheet/`

### Проверьте фронтенд:

Откройте `https://smartleaves.dclouds.ru` и убедитесь что:
- ✅ Категории отображаются в меню
- ✅ Рабочие листы отображаются на главной странице
- ✅ Картинки и превью загружаются
- ✅ PDF файлы можно скачать

## Очистка

После успешного импорта можно удалить временные файлы на сервере:

```bash
cd /var/www/smartleaves
rm -f categories_data.json tags_data.json worksheets_data.json
rm -f import_categories.py import_tags.py import_worksheets.py
rm -f media_files.tar.gz
rm -rf media/  # Директория (файлы уже в Docker volume)
```

## Устранение проблем

### Если импорт прервался

Скрипты можно запускать повторно - они обновят существующие записи, а не создадут дубликаты (проверка по `slug`).

### Если файлы не скопировались

```bash
# Проверьте Docker volume
docker volume inspect smartleaves_media_data

# Проверьте файлы внутри контейнера
docker compose -f docker-compose.prod.yml exec backend ls -lh /app/media/

# Если нужно, скопируйте заново
docker cp media/. smartleaves_backend:/app/media/
```

### Если не хватает места

```bash
# Проверьте свободное место
df -h

# Очистите Docker кэш
docker system prune -af
```

## Размеры данных

- Категории JSON: ~40 КБ
- Теги JSON: ~2 КБ
- Рабочие листы JSON: ~450 КБ
- Медиа файлы (архив): ~50 МБ
- Медиа файлы (распакованные): ~61 МБ

**Итого:** Понадобится минимум **150 МБ** свободного места на сервере.

## Важные замечания

1. ⚠️ **Порядок импорта важен!** Сначала категории, затем теги, потом worksheets
2. ⚠️ **Скопируйте медиа файлы ДО импорта worksheets**
3. ⚠️ **Не прерывайте импорт worksheets** - он занимает 2-3 минуты
4. ✅ Скрипты безопасны для повторного запуска
5. ✅ Все проверки по `slug` - дубликаты не создаются

---

**Время выполнения:** ~5-10 минут в зависимости от скорости интернета и производительности сервера.
