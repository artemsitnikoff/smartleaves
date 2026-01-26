<template>
  <div class="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow overflow-hidden">
    <router-link :to="`/worksheet/${worksheet.slug}`" class="block">
      <!-- Превью -->
      <div class="aspect-[3/4] bg-gray-100 relative overflow-hidden">
        <img
          v-if="worksheet.thumbnail"
          :src="worksheet.thumbnail"
          :alt="worksheet.title"
          class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
        />
        <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
          <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
      </div>

      <!-- Информация -->
      <div class="p-4">
        <h3 class="font-semibold text-lg mb-2 line-clamp-2 hover:text-primary-600 transition-colors">
          {{ worksheet.title }}
        </h3>

        <p class="text-sm text-gray-600 mb-3 line-clamp-2">
          {{ worksheet.description }}
        </p>

        <!-- Категория -->
        <div class="text-xs text-gray-500 mb-2">
          {{ worksheet.category_name }}
        </div>

        <!-- Теги -->
        <div v-if="worksheet.tags.length > 0" class="flex flex-wrap gap-1 mb-3">
          <span
            v-for="tag in worksheet.tags.slice(0, 3)"
            :key="tag.id"
            class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded"
          >
            {{ tag.name }} <span class="text-gray-500">({{ tag.usage_count }})</span>
          </span>
          <span v-if="worksheet.tags.length > 3" class="text-xs text-gray-500">
            +{{ worksheet.tags.length - 3 }}
          </span>
        </div>

        <!-- Статистика -->
        <div class="flex items-center gap-4 text-xs text-gray-500">
          <span class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            {{ worksheet.views_count }}
          </span>
          <span class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            {{ worksheet.downloads_count }}
          </span>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import type { WorksheetListItem } from '@/types'

defineProps<{
  worksheet: WorksheetListItem
}>()
</script>
