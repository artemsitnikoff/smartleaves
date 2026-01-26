<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Вводный текст -->
    <div v-if="settingsStore.settings" class="max-w-4xl mx-auto mb-12">
      <div v-html="settingsStore.settings.home_page_intro" class="prose prose-lg max-w-none"></div>
    </div>

    <!-- Последние рабочие листы -->
    <div class="mb-12">
      <h2 class="text-3xl font-bold mb-6">Последние добавленные</h2>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>

      <div v-else-if="error" class="text-center py-12 text-red-600">
        {{ error }}
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <WorksheetCard
          v-for="worksheet in worksheets"
          :key="worksheet.id"
          :worksheet="worksheet"
        />
      </div>

      <div class="text-center mt-8">
        <router-link
          to="/worksheets"
          class="inline-block bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-lg font-medium transition-colors"
        >
          Смотреть все рабочие листы →
        </router-link>
      </div>
    </div>

    <!-- Популярные категории -->
    <div v-if="categoriesStore.categoryTree.length > 0" class="mb-12">
      <h2 class="text-3xl font-bold mb-6">Категории</h2>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="category in categoriesStore.categoryTree"
          :key="category.id"
          class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <h3 class="text-xl font-bold mb-3">{{ category.name }}</h3>
          <p class="text-gray-600 text-sm mb-4">{{ category.description }}</p>

          <ul class="space-y-2">
            <li v-for="child in category.children" :key="child.id">
              <router-link
                :to="`/category/${child.slug}`"
                class="text-primary-600 hover:text-primary-700 text-sm flex items-center justify-between group"
              >
                <span class="group-hover:underline">{{ child.name }}</span>
                <span class="text-gray-400 text-xs">{{ child.worksheets_count }}</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useCategoriesStore } from '@/stores/categories'
import { worksheetsApi } from '@/api/worksheets'
import WorksheetCard from '@/components/WorksheetCard.vue'
import type { WorksheetListItem } from '@/types'

const settingsStore = useSettingsStore()
const categoriesStore = useCategoriesStore()

const worksheets = ref<WorksheetListItem[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function loadLatestWorksheets() {
  loading.value = true
  error.value = null

  try {
    const response = await worksheetsApi.getList({ page_size: 8 })
    worksheets.value = response.results
  } catch (e) {
    error.value = 'Не удалось загрузить рабочие листы'
    console.error('Failed to fetch worksheets:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  settingsStore.fetchSettings()
  categoriesStore.fetchCategoryTree()
  loadLatestWorksheets()
})
</script>
