import { apiClient } from './client'
import type {
  WorksheetListItem,
  WorksheetDetail,
  PaginatedResponse
} from '@/types'

export interface WorksheetFilters {
  page?: number
  page_size?: number
  category?: number
  category__slug?: string
  grade_level?: string
  difficulty?: string
  search?: string
  ordering?: string
  tags__slug?: string
}

export const worksheetsApi = {
  /**
   * Получить список рабочих листов с фильтрацией и пагинацией
   */
  async getList(filters?: WorksheetFilters): Promise<PaginatedResponse<WorksheetListItem>> {
    const { data } = await apiClient.get('/api/worksheets/', { params: filters })
    return data
  },

  /**
   * Получить детальную информацию о рабочем листе
   */
  async getDetail(slug: string): Promise<WorksheetDetail> {
    const { data } = await apiClient.get(`/api/worksheets/${slug}/`)
    return data
  },

  /**
   * Получить URL для скачивания PDF файла
   */
  getDownloadUrl(id: number): string {
    return `${apiClient.defaults.baseURL}/api/worksheets/${id}/download/`
  },

  /**
   * Скачать PDF файл
   */
  async download(id: number): Promise<Blob> {
    const { data } = await apiClient.get(`/api/worksheets/${id}/download/`, {
      responseType: 'blob',
    })
    return data
  },

  /**
   * Получить похожие рабочие листы из той же категории
   */
  async getSimilar(slug: string): Promise<WorksheetListItem[]> {
    const { data } = await apiClient.get(`/api/worksheets/${slug}/similar/`)
    return data.results || data
  },
}
