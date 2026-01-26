import axios from 'axios'

// Базовый URL для API (можно изменить через переменные окружения)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// Создаем экземпляр axios с базовой конфигурацией
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Добавляем перехватчик ответов для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Здесь можно добавить глобальную обработку ошибок
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)
