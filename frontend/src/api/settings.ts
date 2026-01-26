import { apiClient } from './client'
import type { SiteSettings } from '@/types'

export const settingsApi = {
  /**
   * Получить глобальные настройки сайта
   */
  async get(): Promise<SiteSettings> {
    const { data } = await apiClient.get('/api/settings/')
    return data
  },
}
