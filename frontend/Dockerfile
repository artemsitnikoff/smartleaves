# Frontend Dockerfile для Production (Multi-stage build)

# Stage 1: Build
FROM node:20-alpine AS builder

# Build-time аргументы
ARG VITE_API_URL

WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm ci

# Копирование исходного кода
COPY . .

# Сборка приложения с переменными окружения
ENV VITE_API_URL=$VITE_API_URL
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
