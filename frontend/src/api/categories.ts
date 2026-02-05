import { apiClient } from './client'
import type { Category, CategoryTree } from '@/types'

export const categoriesApi = {
  /**
   * Получить плоский список всех категорий
   */
  async getList(): Promise<Category[]> {
    const { data } = await apiClient.get('/api/categories/')
    // API возвращает пагинированный ответ, берем results
    return data.results || data
  },

  /**
   * Получить иерархическое дерево категорий
   */
  async getTree(): Promise<CategoryTree[]> {
    const { data } = await apiClient.get('/api/categories/tree/')
    // API возвращает пагинированный ответ, берем results
    return data.results || data
  },

  /**
   * Получить детальную информацию о категории с дочерними категориями
   */
  async getDetail(slug: string): Promise<CategoryTree> {
    const { data } = await apiClient.get(`/api/categories/${slug}/`)
    return data
  },
}
