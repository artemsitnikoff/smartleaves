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
    <div v-if="filteredCategories.length > 0" class="mb-12">
      <h2 class="text-3xl font-bold mb-6">Категории</h2>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="category in filteredCategories"
          :key="category.id"
          class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <!-- Заголовок категории с количеством -->
          <router-link
            :to="`/category/${category.slug}`"
            class="block mb-3 group"
          >
            <h3 class="text-xl font-bold group-hover:text-primary-600 transition-colors flex items-center justify-between">
              <span>{{ category.name }}</span>
              <span class="text-gray-400 text-sm font-normal">{{ category.worksheets_count }}</span>
            </h3>
          </router-link>
          <p class="text-gray-600 text-sm mb-4">{{ category.description }}</p>

          <!-- Подкатегории если есть -->
          <ul v-if="category.children && category.children.length > 0" class="space-y-2">
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

          <!-- Если нет подкатегорий - показываем кнопку "Смотреть все" -->
          <div v-else class="mt-2">
            <router-link
              :to="`/category/${category.slug}`"
              class="text-primary-600 hover:text-primary-700 text-sm font-medium inline-flex items-center"
            >
              Смотреть все
              <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
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

// Фильтруем служебные категории (Главная, Генератор и т.д.)
const filteredCategories = computed(() => {
  const excludeSlugs = ['home', 'worksheet-generator']
  return categoriesStore.categoryTree.filter(
    (category) => !excludeSlugs.includes(category.slug)
  )
})

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
