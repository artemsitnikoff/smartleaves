<template>
  <header class="bg-primary-600 text-white shadow-lg">
    <div class="container mx-auto px-4 py-4">
      <!-- Верхняя часть: Логотип и Telegram -->
      <div class="flex justify-between items-center mb-4">
        <!-- Логотип слева -->
        <router-link to="/" class="flex items-center">
          <img src="/leaves.png" alt="Умные листочки" style="height: 100px; width: auto;" />
        </router-link>

        <!-- Иконка Telegram справа -->
        <a
          v-if="settingsStore.settings?.telegram_url"
          :href="settingsStore.settings.telegram_url"
          target="_blank"
          rel="noopener noreferrer"
          class="bg-white hover:bg-gray-100 text-primary-600 p-3 rounded-full transition-colors"
          aria-label="Telegram"
        >
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.295-.6.295-.002 0-.003 0-.005 0l.213-3.054 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.64-.203-.658-.64.135-.954l11.566-4.458c.538-.196 1.006.128.832.941z"/>
          </svg>
        </a>
      </div>

      <!-- Навигация с категориями -->
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
            <div v-else class="relative dropdown-menu">
              <button
                @click.stop="toggleMenu(category.id)"
                class="bg-primary-700 hover:bg-primary-800 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1 whitespace-nowrap"
              >
                {{ category.name }}
                <svg
                  class="w-3 h-3 transition-transform"
                  :class="{ 'rotate-180': openMenuId === category.id }"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Выпадающее меню дочерних категорий -->
              <div
                v-show="openMenuId === category.id"
                class="absolute left-0 mt-2 w-56 bg-white text-gray-800 rounded-lg shadow-xl transition-all duration-200 z-50"
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
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSettingsStore } from '@/stores/settings'
import { useCategoriesStore } from '@/stores/categories'

const settingsStore = useSettingsStore()
const categoriesStore = useCategoriesStore()
const route = useRoute()

// Состояние для отслеживания открытого меню (ID категории)
const openMenuId = ref<number | null>(null)

// Функция для переключения меню
const toggleMenu = (categoryId: number) => {
  openMenuId.value = openMenuId.value === categoryId ? null : categoryId
}

// Закрываем меню при изменении маршрута
watch(() => route.path, () => {
  openMenuId.value = null
})

// Закрываем меню при клике вне его
const closeMenuOnClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.dropdown-menu')) {
    openMenuId.value = null
  }
}

onMounted(() => {
  settingsStore.fetchSettings()
  categoriesStore.fetchCategoryTree()
  document.addEventListener('click', closeMenuOnClickOutside)
})

// Очистка при размонтировании
import { onUnmounted } from 'vue'
onUnmounted(() => {
  document.removeEventListener('click', closeMenuOnClickOutside)
})
</script>
