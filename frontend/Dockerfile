# Frontend Dockerfile для Production (Multi-stage build)

# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm ci

# Копирование исходного кода
COPY . .

# Сборка приложения
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Копирование собранного приложения из builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Копирование кастомной конфигурации Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose порт
EXPOSE 80

# Запуск Nginx
CMD ["nginx", "-g", "daemon off;"]
