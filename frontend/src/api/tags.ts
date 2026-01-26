import { apiClient } from './client'
import type { Tag } from '@/types'

export const tagsApi = {
  /**
   * Получить список всех тегов
   */
  async getList(): Promise<Tag[]> {
    const { data } = await apiClient.get('/api/tags/')
    // API возвращает пагинированный ответ, берем results
    return data.results || data
  },

  /**
   * Получить топ-20 популярных тегов
   */
  async getPopular(): Promise<Tag[]> {
    const { data } = await apiClient.get('/api/tags/popular/')
    // API возвращает пагинированный ответ, берем results
    return data.results || data
  },

  /**
   * Получить детальную информацию о теге
   */
  async getDetail(slug: string): Promise<Tag> {
    const { data } = await apiClient.get(`/api/tags/${slug}/`)
    return data
  },
}
