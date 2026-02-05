<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Заголовок и хлебные крошки -->
    <div class="mb-6">
      <nav class="text-sm text-gray-600 mb-2">
        <router-link to="/" class="hover:text-primary-600">Главная</router-link>
        <span class="mx-2">/</span>
        <span v-if="categorySlug && currentCategory">{{ currentCategory.name }}</span>
        <span v-else-if="tagSlug && currentTag">Тег: {{ currentTag.name }}</span>
        <span v-else>Все рабочие листы</span>
      </nav>

      <h1 class="text-3xl font-bold">
        <span v-if="categorySlug && currentCategory">{{ currentCategory.name }}</span>
        <span v-else-if="tagSlug && currentTag">Рабочие листы с тегом "{{ currentTag.name }}"</span>
        <span v-else>Все рабочие листы</span>
      </h1>

      <p v-if="categorySlug && currentCategory" class="text-gray-600 mt-2">
        {{ currentCategory.description }}
      </p>
    </div>

    <!-- Подкатегории (если есть) -->
    <div v-if="categorySlug && currentCategory?.children && currentCategory.children.length > 0" class="mb-8">
      <h2 class="text-xl font-semibold mb-4">Подкатегории</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
        <router-link
          v-for="child in currentCategory.children"
          :key="child.id"
          :to="`/category/${child.slug}`"
          class="bg-white hover:bg-primary-50 border-2 border-gray-200 hover:border-primary-500 rounded-lg p-4 transition-all text-center group"
        >
          <div class="font-medium text-gray-900 group-hover:text-primary-700 mb-1">
            {{ child.name }}
          </div>
          <div class="text-sm text-gray-500">
            {{ child.worksheets_count }} листов
          </div>
        </router-link>
      </div>
    </div>

    <!-- Основной контент: 70% листы + 30% теги -->
    <div class="grid grid-cols-1 lg:grid-cols-10 gap-8">
      <!-- Список рабочих листов (70%) -->
      <div class="lg:col-span-7">
        <!-- Загрузка -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>

        <!-- Ошибка -->
        <div v-else-if="error" class="text-center py-12 text-red-600">
          {{ error }}
        </div>

        <!-- Пустой результат -->
        <div v-else-if="worksheets.length === 0" class="text-center py-12 text-gray-500">
          <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-lg">Рабочие листы не найдены</p>
        </div>

        <!-- Список -->
        <div v-else>
          <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
            <WorksheetCard
              v-for="worksheet in worksheets"
              :key="worksheet.id"
              :worksheet="worksheet"
            />
          </div>

          <!-- Пагинация -->
          <Pagination
            v-if="pagination"
            :current-page="pagination.current_page"
            :total-pages="pagination.total_pages"
            @page-change="handlePageChange"
          />
        </div>
      </div>

      <!-- Теги (30%) -->
      <div class="lg:col-span-3">
        <div class="bg-white rounded-lg shadow-md p-6 sticky top-4">
          <h2 class="text-xl font-bold mb-4">Теги</h2>

          <!-- Загрузка тегов -->
          <div v-if="tagsLoading" class="text-center py-4">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>

          <!-- Теги -->
          <div v-else-if="tags.length > 0" class="flex flex-wrap gap-2">
            <router-link
              v-for="tag in tags"
              :key="tag.id"
              :to="`/tag/${tag.slug}`"
              :class="[
                'inline-block px-3 py-2 rounded-lg text-sm transition-colors',
                tagSlug === tag.slug
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
              ]"
            >
              {{ tag.name }}
              <span class="text-xs opacity-75">({{ tag.usage_count }})</span>
            </router-link>
          </div>

          <!-- Сбросить фильтр по тегу -->
          <div v-if="tagSlug" class="mt-4 pt-4 border-t">
            <router-link
              to="/worksheets"
              class="block text-center bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded transition-colors"
            >
              Показать все
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { worksheetsApi } from '@/api/worksheets'
import { categoriesApi } from '@/api/categories'
import { tagsApi } from '@/api/tags'
import WorksheetCard from '@/components/WorksheetCard.vue'
import Pagination from '@/components/Pagination.vue'
import type { WorksheetListItem, Category, Tag, PaginatedResponse } from '@/types'

const route = useRoute()

// Получаем slug из route (может быть category или tag)
const categorySlug = computed(() => route.name === 'category' ? route.params.slug as string : null)
const tagSlug = computed(() => route.name === 'tag' ? route.params.slug as string : null)

// Данные
const worksheets = ref<WorksheetListItem[]>([])
const pagination = ref<Omit<PaginatedResponse<WorksheetListItem>, 'results'> | null>(null)
const currentCategory = ref<Category | null>(null)
const currentTag = ref<Tag | null>(null)
const tags = ref<Tag[]>([])

// Состояния загрузки
const loading = ref(false)
const error = ref<string | null>(null)
const tagsLoading = ref(false)

// Текущая страница
const currentPage = ref(1)

async function loadWorksheets() {
  loading.value = true
  error.value = null

  try {
    const filters: any = {
      page: currentPage.value,
    }

    // Если фильтруем по категории
    if (categorySlug.value) {
      // Если у категории есть дочерние категории, собираем все slug'ы
      if (currentCategory.value?.children && currentCategory.value.children.length > 0) {
        const allSlugs = [
          categorySlug.value,
          ...currentCategory.value.children.map(child => child.slug)
        ].join(',')
        filters.category__slug__in = allSlugs
      } else {
        filters.category__slug = categorySlug.value
      }
    }

    // Если фильтруем по тегу
    if (tagSlug.value) {
      filters.tags__slug = tagSlug.value
    }

    const response = await worksheetsApi.getList(filters)
    worksheets.value = response.results
    pagination.value = {
      count: response.count,
      total_pages: response.total_pages,
      current_page: response.current_page,
      page_size: response.page_size,
      next: response.next,
      previous: response.previous,
    }
  } catch (e) {
    error.value = 'Не удалось загрузить рабочие листы'
    console.error('Failed to fetch worksheets:', e)
  } finally {
    loading.value = false
  }
}

async function loadCategory() {
  if (!categorySlug.value) {
    currentCategory.value = null
    return
  }

  try {
    currentCategory.value = await categoriesApi.getDetail(categorySlug.value)
  } catch (e) {
    console.error('Failed to fetch category:', e)
  }
}

async function loadTag() {
  if (!tagSlug.value) {
    currentTag.value = null
    return
  }

  try {
    currentTag.value = await tagsApi.getDetail(tagSlug.value)
  } catch (e) {
    console.error('Failed to fetch tag:', e)
  }
}

async function loadTags() {
  tagsLoading.value = true

  try {
    // Получаем популярные теги
    tags.value = await tagsApi.getPopular()
  } catch (e) {
    console.error('Failed to fetch tags:', e)
  } finally {
    tagsLoading.value = false
  }
}

function handlePageChange(page: number) {
  currentPage.value = page
  loadWorksheets()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Следим за изменениями роута
watch([categorySlug, tagSlug], async () => {
  currentPage.value = 1
  await Promise.all([
    loadCategory(),
    loadTag(),
    loadWorksheets(),
  ])
})

onMounted(async () => {
  await Promise.all([
    loadCategory(),
    loadTag(),
    loadWorksheets(),
    loadTags(),
  ])
})
</script>
