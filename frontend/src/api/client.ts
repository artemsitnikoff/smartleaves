import axios from 'axios'

// Базовый URL для API (можно изменить через переменные окружения)
const API_BASE_URL = import.meta.env.VITE_API_URL || window.location.origin

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
