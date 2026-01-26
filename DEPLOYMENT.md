# Docker Deployment Guide для Smart Leaves

## Преимущества Docker подхода

- ✅ **Воспроизводимость**: Одинаковое окружение на dev, staging и production
- ✅ **Изоляция**: Каждый сервис в своем контейнере
- ✅ **Простота**: Один файл docker-compose для всей инфраструктуры
- ✅ **Масштабируемость**: Легко добавлять новые сервисы
- ✅ **Откат**: Быстрый возврат к предыдущей версии
- ✅ **CI/CD**: Автоматический деплой через GitHub Actions

---

## Требования к VPS

**Минимальные характеристики:**
- CPU: 2 ядра
- RAM: 4 GB
- SSD: 40 GB
- OS: Ubuntu 22.04 LTS или новее

**Рекомендуемые провайдеры:**
- Hetzner (от €4.5/месяц) - лучшее соотношение цена/качество
- DigitalOcean (от $12/месяц)
- Vultr (от $12/месяц)

---

## Пошаговая инструкция

### 1. Первоначальная настройка сервера

```bash
# Подключитесь к серверу
ssh root@your_server_ip

# Обновите систему
apt update && apt upgrade -y

# Создайте пользователя для деплоя
adduser deploy
usermod -aG sudo deploy

# Настройте SSH для нового пользователя
mkdir -p /home/deploy/.ssh
cp ~/.ssh/authorized_keys /home/deploy/.ssh/
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys

# Настройте firewall
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Выйдите и войдите как deploy
exit
ssh deploy@your_server_ip
```

### 2. Установка Docker и Docker Compose

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo apt install -y docker-compose-plugin

# Проверка установки
docker --version
docker compose version

# Выйдите и войдите снова для применения прав
exit
ssh deploy@your_server_ip
```

### 3. Клонирование проекта

```bash
# Создайте директорию для проекта
sudo mkdir -p /var/www/smartleaves
sudo chown deploy:deploy /var/www/smartleaves

# Клонируйте репозиторий
cd /var/www/smartleaves
git clone https://github.com/artemsitnikoff/smartleaves.git .

# Создайте директорию для бэкапов
mkdir -p backups
```

### 4. Настройка переменных окружения

```bash
# Скопируйте example файл
cp .env.prod.example .env.prod

# Отредактируйте переменные
nano .env.prod
```

**Заполните реальными значениями:**
```env
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-generate-new-one
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your_server_ip

DB_NAME=smartleaves
DB_USER=smartleaves
DB_PASSWORD=your-secure-database-password-here

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

VITE_API_URL=https://yourdomain.com
```

**Генерация SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Обновление конфигурации Nginx

```bash
# Отредактируйте nginx конфигурацию
nano nginx/conf.d/default.conf

# Замените "yourdomain.com" на ваш реальный домен
# Если пока нет домена - оставьте как есть
```

### 6. Первый запуск

```bash
# Сделайте deploy скрипт исполняемым
chmod +x deploy.sh

# Запустите контейнеры (первый раз займет время - будет скачивать образы)
./deploy.sh start

# Проверьте статус контейнеров
./deploy.sh status

# Просмотрите логи
./deploy.sh logs
```

### 7. Создание суперпользователя Django

```bash
# Создайте суперпользователя для админ-панели
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Следуйте инструкциям на экране
```

### 8. Настройка DNS

В панели управления доменом создайте A-записи:

```
A Record:
@ → your_server_ip
www → your_server_ip
```

Подождите 5-30 минут пока DNS записи обновятся.

### 9. Получение SSL сертификата

**После того как DNS записи обновились:**

```bash
# Получите SSL сертификат
./deploy.sh ssl your_email@example.com yourdomain.com

# Также для www
docker-compose -f docker-compose.prod.yml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email your_email@example.com \
  --agree-tos \
  --no-eff-email \
  -d www.yourdomain.com
```

**Обновите конфигурацию Nginx:**

```bash
# Отредактируйте конфигурацию
nano nginx/conf.d/default.conf

# Раскомментируйте секции с HTTPS (удалите # в начале строк)
# Замените "yourdomain.com" на ваш домен

# Перезапустите nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### 10. Настройка автоматического деплоя (CI/CD)

**На локальной машине:**

```bash
# Создайте SSH ключ для GitHub Actions
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_smartleaves

# Скопируйте публичный ключ на сервер
ssh-copy-id -i ~/.ssh/github_smartleaves.pub deploy@your_server_ip

# Выведите приватный ключ (скопируйте весь вывод)
cat ~/.ssh/github_smartleaves
```

**В GitHub:**

1. Перейдите в Settings → Secrets and variables → Actions
2. Создайте secrets:
   - `SERVER_HOST` = ваш IP или домен
   - `SERVER_USER` = deploy
   - `SSH_PRIVATE_KEY` = весь приватный ключ (включая BEGIN и END строки)

3. Теперь при каждом push в main ветку будет автоматический деплой!

---

## Управление проектом

### Полезные команды

```bash
# Посмотреть статус контейнеров
./deploy.sh status

# Посмотреть логи всех сервисов
./deploy.sh logs

# Посмотреть логи конкретного сервиса
./deploy.sh logs backend
./deploy.sh logs nginx

# Перезапустить все контейнеры
./deploy.sh restart

# Пересобрать и перезапустить (после изменений в коде)
./deploy.sh rebuild

# Запустить миграции
./deploy.sh migrate

# Открыть Django shell
./deploy.sh shell

# Создать бэкап базы данных
./deploy.sh backup

# Остановить все контейнеры
./deploy.sh stop

# Запустить контейнеры
./deploy.sh start

# Очистить неиспользуемые Docker ресурсы
./deploy.sh clean
```

### Прямые Docker команды

```bash
# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f nginx

# Выполнение команд внутри контейнера
docker-compose -f docker-compose.prod.yml exec backend python manage.py shell
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker-compose -f docker-compose.prod.yml exec db psql -U smartleaves

# Перезапуск конкретного сервиса
docker-compose -f docker-compose.prod.yml restart backend
docker-compose -f docker-compose.prod.yml restart nginx
```

---

## Резервное копирование

### Автоматический бэкап

Создайте cron job для ежедневного бэкапа:

```bash
# Откройте crontab
crontab -e

# Добавьте строку (бэкап каждый день в 2:00 AM)
0 2 * * * cd /var/www/smartleaves && ./deploy.sh backup >> /var/log/smartleaves_backup.log 2>&1
```

### Ручной бэкап

```bash
# База данных
./deploy.sh backup

# Медиа файлы
tar -czf backups/media_$(date +%Y%m%d).tar.gz -C /var/lib/docker/volumes/smartleaves_media_data/_data .
```

### Восстановление из бэкапа

```bash
# Восстановление базы данных
cat backups/db_backup_YYYYMMDD_HHMMSS.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U smartleaves smartleaves

# Восстановление медиа файлов
tar -xzf backups/media_YYYYMMDD.tar.gz -C /var/lib/docker/volumes/smartleaves_media_data/_data
```

---

## Обновление проекта

### Автоматическое (через GitHub Actions)

Просто запушьте изменения в main ветку:

```bash
git push origin main
```

GitHub Actions автоматически задеплоит на сервер.

### Ручное обновление

```bash
cd /var/www/smartleaves

# Подтянуть изменения
git pull origin main

# Пересобрать и перезапустить
./deploy.sh rebuild
```

---

## Мониторинг

### Проверка здоровья системы

```bash
# Статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# Использование ресурсов
docker stats

# Дисковое пространство
df -h
docker system df

# Логи системы
journalctl -u docker -f
```

### Полезные endpoint'ы для мониторинга

- Админ-панель Django: `https://yourdomain.com/admin/`
- API: `https://yourdomain.com/api/`
- Фронтенд: `https://yourdomain.com/`

---

## Решение проблем

### Контейнер не запускается

```bash
# Посмотрите логи
./deploy.sh logs backend

# Проверьте конфигурацию
docker-compose -f docker-compose.prod.yml config

# Пересоберите образ
./deploy.sh rebuild
```

### База данных недоступна

```bash
# Проверьте статус
docker-compose -f docker-compose.prod.yml exec db pg_isready -U smartleaves

# Посмотрите логи
./deploy.sh logs db

# Перезапустите
docker-compose -f docker-compose.prod.yml restart db
```

### Nginx показывает 502 Bad Gateway

```bash
# Проверьте что backend работает
docker-compose -f docker-compose.prod.yml ps backend

# Посмотрите логи backend
./deploy.sh logs backend

# Посмотрите логи nginx
./deploy.sh logs nginx
```

### Закончилось место на диске

```bash
# Очистите Docker ресурсы
./deploy.sh clean

# Удалите старые бэкапы
find backups/ -type f -mtime +30 -delete

# Проверьте использование
docker system df
df -h
```

---

## Масштабирование

### Увеличение worker'ов Gunicorn

Отредактируйте `backend/Dockerfile`:

```dockerfile
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "5"]
```

Количество workers = (CPU cores * 2) + 1

### Добавление Redis для кэширования

Добавьте в `docker-compose.prod.yml`:

```yaml
redis:
  image: redis:alpine
  restart: always
  networks:
    - smartleaves_network
```

---

## Безопасность

✅ **Что уже настроено:**
- Firewall (только 22, 80, 443 порты)
- SSL/TLS шифрование
- Изолированные контейнеры
- Непривилегированные пользователи в контейнерах

✅ **Дополнительные рекомендации:**
- Регулярно обновляйте Docker образы
- Используйте сложные пароли
- Настройте fail2ban
- Мониторьте логи на подозрительную активность

---

## Поддержка

При возникновении проблем:
1. Проверьте логи: `./deploy.sh logs`
2. Проверьте статус: `./deploy.sh status`
3. Проверьте конфигурацию: `docker-compose -f docker-compose.prod.yml config`

---

**Успешного деплоя! 🚀**
