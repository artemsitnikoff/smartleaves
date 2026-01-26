<template>
  <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-8">
    <!-- Предыдущая страница -->
    <button
      @click="$emit('page-change', currentPage - 1)"
      :disabled="currentPage === 1"
      class="px-4 py-2 rounded border disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition-colors"
    >
      ← Назад
    </button>

    <!-- Страницы -->
    <div class="flex gap-2">
      <button
        v-for="page in visiblePages"
        :key="page"
        @click="page !== '...' && $emit('page-change', page)"
        :class="[
          'px-4 py-2 rounded border transition-colors',
          page === currentPage
            ? 'bg-primary-600 text-white border-primary-600'
            : 'hover:bg-gray-100',
          page === '...' && 'cursor-default hover:bg-white'
        ]"
        :disabled="page === '...'"
      >
        {{ page }}
      </button>
    </div>

    <!-- Следующая страница -->
    <button
      @click="$emit('page-change', currentPage + 1)"
      :disabled="currentPage === totalPages"
      class="px-4 py-2 rounded border disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition-colors"
    >
      Вперед →
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  currentPage: number
  totalPages: number
}>()

defineEmits<{
  'page-change': [page: number]
}>()

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const { currentPage, totalPages } = props

  if (totalPages <= 7) {
    // Показываем все страницы, если их мало
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i)
    }
  } else {
    // Показываем первую, последнюю и страницы вокруг текущей
    if (currentPage <= 3) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(totalPages)
    } else if (currentPage >= totalPages - 2) {
      pages.push(1)
      pages.push('...')
      for (let i = totalPages - 4; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = currentPage - 1; i <= currentPage + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(totalPages)
    }
  }

  return pages
})
</script>
