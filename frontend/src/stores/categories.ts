import { defineStore } from 'pinia'
import { ref } from 'vue'
import { categoriesApi } from '@/api/categories'
import type { CategoryTree } from '@/types'

export const useCategoriesStore = defineStore('categories', () => {
  const categoryTree = ref<CategoryTree[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchCategoryTree() {
    if (categoryTree.value.length > 0) return // Уже загружено

    loading.value = true
    error.value = null

    try {
      categoryTree.value = await categoriesApi.getTree()
    } catch (e) {
      error.value = 'Не удалось загрузить категории'
      console.error('Failed to fetch categories:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    categoryTree,
    loading,
    error,
    fetchCategoryTree,
  }
})
