import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    settings: {
      historyCount: 10,
      temperature: 0.7,
      maxTokens: 2000,
      apiKey: '',
      apiUrl: 'https://api.kfm.plus/v1/chat/completions',
    },
  }),

  actions: {
    updateSettings(newSettings: Partial<typeof this.settings>) {
      this.settings = { ...this.settings, ...newSettings }
    },
  },
})

