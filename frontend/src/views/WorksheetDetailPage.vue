<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Загрузка -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="text-center py-12 text-red-600">
      {{ error }}
    </div>

    <!-- Детали рабочего листа -->
    <div v-else-if="worksheet" class="max-w-6xl mx-auto">
      <!-- Хлебные крошки -->
      <nav class="text-sm text-gray-600 mb-4">
        <router-link to="/" class="hover:text-primary-600">Главная</router-link>
        <span class="mx-2">/</span>
        <router-link
          v-if="worksheet.category"
          :to="`/category/${worksheet.category.slug}`"
          class="hover:text-primary-600"
        >
          {{ worksheet.category.name }}
        </router-link>
        <span class="mx-2">/</span>
        <span>{{ worksheet.title }}</span>
      </nav>

      <!-- Основной контент -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Превью и кнопка скачивания -->
        <div>
          <div class="bg-white rounded-lg shadow-lg overflow-hidden mb-4">
            <button
              @click="handleDownload"
              class="group relative w-full cursor-pointer block"
              :disabled="downloading"
            >
              <img
                v-if="worksheet.preview_image"
                :src="worksheet.preview_image"
                :alt="worksheet.title"
                class="w-full block"
              />
              <div v-else class="aspect-[3/4] bg-gray-100 flex items-center justify-center">
                <svg class="w-24 h-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>

              <!-- Overlay - всегда видно, при hover темнее -->
              <div class="absolute inset-0 bg-black opacity-10 group-hover:opacity-40 transition-opacity pointer-events-none"></div>

              <!-- Иконка скачивания - всегда видна -->
              <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div class="bg-white rounded-full p-4 shadow-lg">
                  <svg class="w-12 h-12 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                </div>
              </div>

              <!-- Индикатор загрузки -->
              <div v-if="downloading" class="absolute inset-0 bg-white bg-opacity-90 flex items-center justify-center z-10">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
              </div>
            </button>
          </div>

          <!-- Кнопка скачивания -->
          <button
            @click="handleDownload"
            :disabled="downloading"
            class="w-full bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            {{ downloading ? 'Загрузка...' : 'Скачать PDF' }}
          </button>

          <!-- Статистика -->
          <div class="mt-4 flex items-center justify-around text-sm text-gray-600">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <span>Просмотров: {{ worksheet.views_count }}</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>Скачиваний: {{ worksheet.downloads_count }}</span>
            </div>
          </div>
        </div>

        <!-- Информация -->
        <div>
          <h1 class="text-3xl font-bold mb-4">{{ worksheet.title }}</h1>

          <p class="text-gray-700 mb-6">{{ worksheet.description }}</p>

          <!-- Характеристики -->
          <div class="space-y-3 mb-6">
            <div class="flex items-center gap-3">
              <span class="font-semibold text-gray-700">Категория:</span>
              <router-link
                v-if="worksheet.category"
                :to="`/category/${worksheet.category.slug}`"
                class="text-primary-600 hover:text-primary-700"
              >
                {{ worksheet.category.name }}
              </router-link>
            </div>

            <div class="flex items-center gap-3">
              <span class="font-semibold text-gray-700">Уровень:</span>
              <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                {{ gradeLevelLabel(worksheet.grade_level) }}
              </span>
            </div>

            <div class="flex items-center gap-3">
              <span class="font-semibold text-gray-700">Сложность:</span>
              <span :class="difficultyClass(worksheet.difficulty)">
                {{ difficultyLabel(worksheet.difficulty) }}
              </span>
            </div>
          </div>

          <!-- Теги -->
          <div v-if="worksheet.tags.length > 0" class="mb-6">
            <h3 class="font-semibold text-gray-700 mb-3">Теги:</h3>
            <div class="flex flex-wrap gap-2">
              <router-link
                v-for="tag in worksheet.tags"
                :key="tag.id"
                :to="`/tag/${tag.slug}`"
                class="inline-block px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm transition-colors"
              >
                {{ tag.name }} <span class="text-gray-500">({{ tag.usage_count }})</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Похожие рабочие листы --><div v-if="similarWorksheets.length > 0" class="mt-12">
        <h2 class="text-2xl font-bold mb-6">Похожие рабочие листы</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <WorksheetCard
            v-for="similar in similarWorksheets"
            :key="similar.id"
            :worksheet="similar"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { worksheetsApi } from '@/api/worksheets'
import type { WorksheetDetail, WorksheetListItem, GradeLevel, Difficulty } from '@/types'
import WorksheetCard from '@/components/WorksheetCard.vue'

const route = useRoute()
const slug = route.params.slug as string

const worksheet = ref<WorksheetDetail | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const downloading = ref(false)
const similarWorksheets = ref<WorksheetListItem[]>([])

async function loadWorksheet() {
  loading.value = true
  error.value = null

  try {
    worksheet.value = await worksheetsApi.getDetail(slug)
    // Загружаем похожие рабочие листы
    await loadSimilarWorksheets()
  } catch (e) {
    error.value = 'Не удалось загрузить рабочий лист'
    console.error('Failed to fetch worksheet:', e)
  } finally {
    loading.value = false
  }
}

async function loadSimilarWorksheets() {
  try {
    similarWorksheets.value = await worksheetsApi.getSimilar(slug)
  } catch (e) {
    console.error('Failed to fetch similar worksheets:', e)
  }
}

async function handleDownload() {
  if (!worksheet.value || downloading.value) return

  downloading.value = true

  try {
    const blob = await worksheetsApi.download(worksheet.value.id)

    // Создаем ссылку для скачивания
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${worksheet.value.slug}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    // Увеличиваем счетчик скачиваний локально
    worksheet.value.downloads_count++
  } catch (e) {
    console.error('Failed to download PDF:', e)
    alert('Не удалось скачать файл. Попробуйте еще раз.')
  } finally {
    downloading.value = false
  }
}

function gradeLevelLabel(level: GradeLevel): string {
  const labels: Record<GradeLevel, string> = {
    preschool: 'Дошкольники (3-4 года)',
    kindergarten: 'Подготовительная группа (5-6 лет)',
    grade1: '1 класс',
    grade2: '2 класс',
    grade3: '3 класс',
    grade4: '4 класс',
    grade5: '5 класс',
  }
  return labels[level] || level
}

function difficultyLabel(difficulty: Difficulty): string {
  const labels: Record<Difficulty, string> = {
    easy: 'Легкий',
    medium: 'Средний',
    hard: 'Сложный',
  }
  return labels[difficulty] || difficulty
}

function difficultyClass(difficulty: Difficulty): string {
  const classes: Record<Difficulty, string> = {
    easy: 'px-3 py-1 bg-green-100 text-green-800 rounded',
    medium: 'px-3 py-1 bg-yellow-100 text-yellow-800 rounded',
    hard: 'px-3 py-1 bg-red-100 text-red-800 rounded',
  }
  return classes[difficulty] || ''
}

onMounted(() => {
  loadWorksheet()
})
</script>
