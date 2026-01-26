<template>
  <footer class="bg-gray-800 text-white mt-12">
    <div class="container mx-auto px-4 py-8">
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Информация -->
        <div>
          <h3 class="text-xl font-bold mb-4">Умные листочки</h3>
          <p v-if="settingsStore.settings" class="text-gray-300">
            {{ settingsStore.settings.footer_text }}
          </p>
        </div>

        <!-- Контакты -->
        <div>
          <h3 class="text-xl font-bold mb-4">Контакты</h3>
          <div v-if="settingsStore.settings" class="space-y-2 text-gray-300">
            <p v-if="settingsStore.settings.contact_email">
              Email: <a :href="`mailto:${settingsStore.settings.contact_email}`" class="hover:text-primary-400">
                {{ settingsStore.settings.contact_email }}
              </a>
            </p>
            <p v-if="settingsStore.settings.contact_phone">
              Телефон: {{ settingsStore.settings.contact_phone }}
            </p>
            <div v-if="settingsStore.settings.telegram_url" class="pt-2">
              <a :href="settingsStore.settings.telegram_url" target="_blank" rel="noopener noreferrer"
                 class="inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 px-4 py-2 rounded transition-colors">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.461-1.901-.903-1.056-.693-1.653-1.124-2.678-1.8-1.185-.781-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.009-1.252-.242-1.865-.442-.752-.244-1.349-.374-1.297-.789.027-.216.324-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.14.121.099.155.232.171.327.016.095.037.312.021.481z"/>
                </svg>
                Telegram
              </a>
            </div>
          </div>
        </div>

        <!-- Навигация -->
        <div>
          <h3 class="text-xl font-bold mb-4">Информация</h3>
          <ul class="space-y-2">
            <li>
              <router-link to="/about" class="text-gray-300 hover:text-primary-400 transition-colors">
                О проекте
              </router-link>
            </li>
            <li>
              <router-link to="/contacts" class="text-gray-300 hover:text-primary-400 transition-colors">
                Контакты
              </router-link>
            </li>
            <li>
              <router-link to="/terms" class="text-gray-300 hover:text-primary-400 transition-colors">
                Правила использования
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- Копирайт -->
      <div class="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
        <p>© {{ new Date().getFullYear() }} Умные листочки. Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()

onMounted(() => {
  settingsStore.fetchSettings()
})
</script>
