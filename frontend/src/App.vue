<template>
  <div id="app" class="min-h-screen flex flex-col bg-gray-50">
    <AppHeader />

    <main class="flex-grow">
      <RouterView />
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>
