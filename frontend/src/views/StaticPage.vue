<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-6">{{ pageTitle }}</h1>

      <div class="bg-white rounded-lg shadow-md p-8 prose prose-lg max-w-none">
        <p>{{ pageContent }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const pageTitle = computed(() => {
  switch (route.name) {
    case 'about':
      return 'О проекте'
    case 'contacts':
      return 'Контакты'
    case 'terms':
      return 'Правила использования контента'
    default:
      return 'Страница'
  }
})

const pageContent = computed(() => {
  switch (route.name) {
    case 'about':
      return 'Информация о проекте. Эта страница редактируется через Wagtail CMS в разделе Pages.'
    case 'contacts':
      return 'Контактная информация. Эта страница редактируется через Wagtail CMS в разделе Pages.'
    case 'terms':
      return 'Правила использования контента. Эта страница редактируется через Wagtail CMS в разделе Pages.'
    default:
      return 'Контент загружается...'
  }
})
</script>
