<template>
  <header class="bg-primary-600 text-white shadow-lg">
    <div class="container mx-auto px-4 py-6">
      <!-- Заголовок сайта -->
      <div class="text-center mb-4">
        <router-link to="/" class="inline-block">
          <h1 class="text-4xl font-bold">Умные листочки</h1>
        </router-link>
        <p v-if="settingsStore.settings" class="text-primary-100 mt-2">
          {{ settingsStore.settings.header_text }}
        </p>
      </div>

      <!-- Навигация с категориями (в 2 строки) -->
      <nav class="flex flex-wrap justify-center items-center gap-1 max-w-7xl mx-auto">
        <div v-if="categoriesStore.loading" class="text-primary-100">
          Загрузка категорий...
        </div>
        <div v-else-if="categoriesStore.error" class="text-red-300">
          {{ categoriesStore.error }}
        </div>
        <template v-else>
          <div v-for="category in categoriesStore.categoryTree" :key="category.id">
            <!-- Категория без детей - простая ссылка -->
            <router-link
              v-if="!category.children || category.children.length === 0"
              :to="`/category/${category.slug}`"
              class="bg-primary-700 hover:bg-primary-800 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
            >
              {{ category.name }}
            </router-link>

            <!-- Категория с детьми - с выпадающим меню -->
            <div v-else class="relative group">
              <router-link
                :to="`/category/${category.slug}`"
                class="bg-primary-700 hover:bg-primary-800 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1 whitespace-nowrap"
              >
                {{ category.name }}
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </router-link>

              <!-- Выпадающее меню дочерних категорий -->
              <div
                class="absolute left-0 mt-2 w-56 bg-white text-gray-800 rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50"
              >
                <div class="py-2">
                  <router-link
                    v-for="child in category.children"
                    :key="child.id"
                    :to="`/category/${child.slug}`"
                    class="block px-4 py-2 hover:bg-primary-50 hover:text-primary-700 transition-colors"
                  >
                    {{ child.name }}
                    <span class="text-gray-500 text-sm ml-1">({{ child.worksheets_count }})</span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { useCategoriesStore } from '@/stores/categories'

const settingsStore = useSettingsStore()
const categoriesStore = useCategoriesStore()

onMounted(() => {
  settingsStore.fetchSettings()
  categoriesStore.fetchCategoryTree()
})
</script>
