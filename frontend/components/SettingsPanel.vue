<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-end">
    <div class="w-96 bg-primary h-full overflow-y-auto p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold">设置</h2>
        <button @click="$emit('close')" class="p-2 hover:bg-secondary rounded-lg">
          <X class="w-5 h-5" />
        </button>
      </div>
      
      <!-- Theme -->
      <div class="mb-6">
        <h3 class="text-lg font-medium mb-3">主题</h3>
        <label class="flex items-center gap-2">
          <input
            type="checkbox"
            v-model="isDark"
            @change="toggleTheme"
            class="w-4 h-4"
          />
          <span>暗色主题</span>
        </label>
      </div>
      
      <!-- AI Parameters -->
      <div class="mb-6">
        <h3 class="text-lg font-medium mb-3">AI 参数</h3>
        <div class="space-y-3">
          <div>
            <label class="block text-sm mb-1">历史记录条数</label>
            <input
              v-model.number="settings.historyCount"
              type="number"
              class="w-full px-3 py-2 border border-border rounded-lg bg-primary"
            />
          </div>
          <div>
            <label class="block text-sm mb-1">温度 (Temperature)</label>
            <input
              v-model.number="settings.temperature"
              type="number"
              step="0.1"
              min="0"
              max="2"
              class="w-full px-3 py-2 border border-border rounded-lg bg-primary"
            />
          </div>
          <div>
            <label class="block text-sm mb-1">最大 Token 数</label>
            <input
              v-model.number="settings.maxTokens"
              type="number"
              class="w-full px-3 py-2 border border-border rounded-lg bg-primary"
            />
          </div>
        </div>
      </div>
      
      <!-- API Config -->
      <div class="mb-6">
        <h3 class="text-lg font-medium mb-3">API 配置</h3>
        <div class="space-y-3">
          <div>
            <label class="block text-sm mb-1">API Key</label>
            <input
              v-model="settings.apiKey"
              type="password"
              class="w-full px-3 py-2 border border-border rounded-lg bg-primary"
            />
          </div>
          <div>
            <label class="block text-sm mb-1">API URL</label>
            <input
              v-model="settings.apiUrl"
              type="text"
              class="w-full px-3 py-2 border border-border rounded-lg bg-primary"
            />
          </div>
        </div>
      </div>
      
      <!-- Save Button -->
      <button
        @click="saveSettings"
        class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        保存设置
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useThemeStore } from '~/stores/theme'
import { useSettingsStore } from '~/stores/settings'
import { X } from 'lucide-vue-next'

const themeStore = useThemeStore()
const settingsStore = useSettingsStore()

const isDark = ref(false)
const settings = ref({
  historyCount: 10,
  temperature: 0.7,
  maxTokens: 2000,
  apiKey: '',
  apiUrl: 'https://api.kfm.plus/v1/chat/completions',
})

const toggleTheme = () => {
  themeStore.toggleTheme()
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

const saveSettings = () => {
  settingsStore.updateSettings(settings.value)
  alert('设置已保存')
}

onMounted(() => {
  isDark.value = themeStore.isDark
  Object.assign(settings.value, settingsStore.settings)
})
</script>

