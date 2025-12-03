import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    settings: {
      historyCount: 10,
      temperature: 0.7,
      maxTokens: 2000,
    },
  }),

  actions: {
    updateSettings(newSettings: Partial<typeof this.settings>) {
      this.settings = { ...this.settings, ...newSettings }
    },
  },
})

