#!/bin/bash

# Скрипт для управления Docker deployment
# Использование: ./deploy.sh [command]

set -e

COMPOSE_FILE="docker-compose.prod.yml"

# Определяем команду docker compose (поддержка старой и новой версии)
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

case "$1" in
  start)
    echo "🚀 Starting containers..."
    $DOCKER_COMPOSE -f $COMPOSE_FILE up -d
    echo "✅ Containers started!"
    $DOCKER_COMPOSE -f $COMPOSE_FILE ps
    ;;

  stop)
    echo "🛑 Stopping containers..."
    $DOCKER_COMPOSE -f $COMPOSE_FILE down
    echo "✅ Containers stopped!"
    ;;

  restart)
    echo "🔄 Restarting containers..."
    $DOCKER_COMPOSE -f $COMPOSE_FILE restart
    echo "✅ Containers restarted!"
    $DOCKER_COMPOSE -f $COMPOSE_FILE ps
    ;;

  rebuild)
    echo "🏗️  Rebuilding and restarting containers..."
    $DOCKER_COMPOSE -f $COMPOSE_FILE down
    $DOCKER_COMPOSE -f $COMPOSE_FILE build --no-cache
    $DOCKER_COMPOSE -f $COMPOSE_FILE up -d
    echo "✅ Containers rebuilt and started!"
    $DOCKER_COMPOSE -f $COMPOSE_FILE ps
    ;;

  logs)
    if [ -z "$2" ]; then
      $DOCKER_COMPOSE -f $COMPOSE_FILE logs -f
    else
      $DOCKER_COMPOSE -f $COMPOSE_FILE logs -f $2
    fi
    ;;

  status)
    echo "📊 Container status:"
    $DOCKER_COMPOSE -f $COMPOSE_FILE ps
    ;;

  migrate)
    echo "🔄 Running migrations..."
    $DOCKER_COMPOSE -f $COMPOSE_FILE exec backend python manage.py migrate
    echo "✅ Migrations completed!"
    ;;

  shell)
    echo "🐚 Opening Django shell..."
    $DOCKER_COMPOSE -f $COMPOSE_FILE exec backend python manage.py shell
    ;;

  backup)
    echo "💾 Creating database backup..."
    BACKUP_DIR="./backups"
    mkdir -p $BACKUP_DIR
    BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"
    $DOCKER_COMPOSE -f $COMPOSE_FILE exec -T db pg_dump -U smartleaves smartleaves > $BACKUP_FILE
    echo "✅ Backup saved to: $BACKUP_FILE"
    ;;

  ssl)
    echo "🔐 Obtaining SSL certificate..."
    $DOCKER_COMPOSE -f $COMPOSE_FILE run --rm certbot certonly \
      --webroot \
      --webroot-path=/var/www/certbot \
      --email $2 \
      --agree-tos \
      --no-eff-email \
      -d $3
    echo "✅ SSL certificate obtained!"
    echo "Don't forget to update nginx configuration and restart nginx!"
    ;;

  clean)
    echo "🧹 Cleaning up unused Docker resources..."
    docker system prune -af --volumes
    echo "✅ Cleanup completed!"
    ;;

  *)
    echo "Smart Leaves Docker Deployment Manager"
    echo ""
    echo "Usage: ./deploy.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start          Start all containers"
    echo "  stop           Stop all containers"
    echo "  restart        Restart all containers"
    echo "  rebuild        Rebuild and restart all containers"
    echo "  logs [service] View logs (optionally for specific service)"
    echo "  status         Show container status"
    echo "  migrate        Run Django migrations"
    echo "  shell          Open Django shell"
    echo "  backup         Create database backup"
    echo "  ssl <email> <domain>  Obtain SSL certificate"
    echo "  clean          Clean up unused Docker resources"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh start"
    echo "  ./deploy.sh logs backend"
    echo "  ./deploy.sh ssl admin@example.com example.com"
    ;;
esac
