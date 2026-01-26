import { defineStore } from 'pinia'
import { ref } from 'vue'
import { settingsApi } from '@/api/settings'
import type { SiteSettings } from '@/types'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<SiteSettings | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchSettings() {
    if (settings.value) return // Уже загружено

    loading.value = true
    error.value = null

    try {
      settings.value = await settingsApi.get()
    } catch (e) {
      error.value = 'Не удалось загрузить настройки сайта'
      console.error('Failed to fetch settings:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    settings,
    loading,
    error,
    fetchSettings,
  }
})
