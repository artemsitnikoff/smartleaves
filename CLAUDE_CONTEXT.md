# Claude AI - Быстрый контекст проекта

## ⚡ Основное
**Проект:** Smart Leaves (Умные листочки) - образовательные worksheet для детей
**Owner:** Artem (математик, CEO)
**Stack:** Django 5.0 + Wagtail 6.0 + Vue 3 + TypeScript + Tailwind v4
**Статус:** Прототип, ~900 worksheet в базе

## 🎯 Что это?
Аналог kiddoworksheets.com - бесплатная платформа для скачивания образовательных PDF worksheet.
Категории и контент на английском языке.

## 📂 Структура
```
backend/          # Django + Wagtail (порт 8000)
├── apps/
│   ├── categories/  # 2-уровневая иерархия (40 категорий)
│   ├── tags/        # 24 тега с auto-counting
│   ├── worksheets/  # ~900 worksheet с PDF и preview
│   └── cms/         # Wagtail: настройки, статические страницы

frontend/         # Vue 3 + TypeScript (порт 5173)
├── src/
│   ├── api/         # Axios клиенты
│   ├── components/  # AppHeader, WorksheetCard, Pagination
│   ├── views/       # HomePage, WorksheetListPage, WorksheetDetailPage
│   └── stores/      # Pinia: settings, categories

venv/            # Python окружение
```

## 🔑 Ключевые особенности

### Модели
- **Category:** 2 уровня max, `order` для сортировки, `get_worksheets_count()`
- **Tag:** ManyToMany с Worksheet, auto `usage_count` через signals
- **Worksheet:** PDF + thumbnail (300x400) + preview (800x1000), статистика views/downloads
- **SiteSettings:** Wagtail настройки, `worksheets_per_page=21` (делится на 3)

### API фильтры
- `?category__slug=alphabets` - по slug категории
- `?tags__slug=age-3-4` - по slug тега
- `?search=math` - полнотекстовый поиск
- Пагинация: 21 элемент на странице

### Frontend особенности
- **Tailwind v4:** новый синтаксис `@import "tailwindcss"` + `@theme {}`
- **Image URLs:** DRF возвращает полные URL, НЕ добавлять VITE_API_URL!
- **Menu:** Категории 1 уровня горизонтально, с детьми - dropdown
- **Grid:** 3 колонки worksheet, 7 рядов на странице
- **Preview overlay:** 10% opacity постоянно → 40% при hover, иконка всегда видна

## 🚀 Запуск

### Backend
```bash
cd backend
source ../venv/bin/activate
python manage.py runserver
```
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/api/docs/
- Wagtail: http://127.0.0.1:8000/admin/ (admin/admin123)

### Frontend
```bash
cd frontend
npm run dev
```
- App: http://localhost:5173

## 🛠️ Команды

```bash
# Загрузить категории из JSON
python manage.py load_categories_from_json

# Сгенерировать 300 worksheet
python manage.py generate_100_worksheets --count=300

# Сгенерировать preview для всех
python manage.py generate_previews
```

## ⚠️ Важные детали

1. **Пагинация:** 21 элемент (делится на 3), не 20!
2. **Tailwind v4:** Новый синтаксис, без config файла
3. **Image URLs:** Уже полные от DRF, не конкатенировать
4. **Категории:** Max 2 уровня, валидация в clean()
5. **Tags usage_count:** Автообновление через signals
6. **Фильтры:** Используй `__slug` для связей (category__slug, tags__slug)
7. **Social:** Только Telegram, Facebook/Instagram удалены

## 🐛 Частые ошибки

- ❌ `import.meta.env` в template → ✅ Создать переменную в script
- ❌ Дублирование URL для картинок → ✅ DRF уже возвращает полный URL
- ❌ Overlay скрывает картинку → ✅ Использовать отдельные слои с pointer-events-none
- ❌ category: id в фильтрах → ✅ category__slug для slug

## 📊 Текущие данные

- Worksheet: ~900 (генерация 500 в процессе)
- Категории: 40 (Home, Alphabets, Numbers, Maths, Vocabulary, Shapes, Coloring...)
- Теги: 24 (Age groups, Grades, Difficulty, Types)
- PDF: Все с уникальным дизайном (reportlab)
- Preview: Все с рандомными цветами (Pillow)

## 📁 Важные файлы

- `backend/apps/categories/models.py` - Валидация 2-уровневой иерархии
- `backend/apps/worksheets/pagination.py` - page_size = 21
- `frontend/src/style.css` - Tailwind v4 синтаксис
- `frontend/src/components/AppHeader.vue` - Горизонтальное меню
- `categories.json` - Структура категорий

## 🔐 Credentials

- Superuser: admin / admin123
- SECRET_KEY: adkyl=8!5nvh+3(*xx27l%_c(b9*-f8)tg4+f#d+otkmb#=d9h
- VITE_API_URL: http://127.0.0.1:8000

---

**Последнее обновление:** 2026-01-26
**Рабочая директория:** /Users/artemsitnikov/SmartLeaves/
